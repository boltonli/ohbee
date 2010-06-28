/**********
This library is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the
Free Software Foundation; either version 2.1 of the License, or (at your
option) any later version. (See <http://www.gnu.org/copyleft/lesser.html>.)

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this library; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
**********/
// Copyright (c) 1996-2010, Live Networks, Inc.  All rights reserved
// A test program that streams a WAV audio file via RTP/RTCP
// main program

#include "liveMedia.hh"
#include "GroupsockHelper.hh"

#include "BasicUsageEnvironment.hh"

// To convert 16-bit samples to 8-bit u-law ("u" is the Greek letter "mu")
// encoding, before streaming, uncomment the following line:
//#define CONVERT_TO_ULAW 1

UsageEnvironment* env;

void play(); // forward

int main(int argc, char** argv) {
  // Begin by setting up our usage environment:
  TaskScheduler* scheduler = BasicTaskScheduler::createNew();
  env = BasicUsageEnvironment::createNew(*scheduler);

  play();

  env->taskScheduler().doEventLoop(); // does not return
  return 0; // only to prevent compiler warnings
}

char const* inputFileName = "test.wav";

void afterPlaying(void* clientData); // forward

// A structure to hold the state of the current session.
// It is used in the "afterPlaying()" function to clean up the session.
struct sessionState_t {
  FramedSource* source;
  RTPSink* sink;
  RTCPInstance* rtcpInstance;
  Groupsock* rtpGroupsock;
  Groupsock* rtcpGroupsock;
  RTSPServer* rtspServer;
} sessionState;

void play() {
  // Open the file as a 'WAV' file:
  WAVAudioFileSource* pcmSource
    = WAVAudioFileSource::createNew(*env, inputFileName);
  if (pcmSource == NULL) {
    *env << "Unable to open file \"" << inputFileName
	 << "\" as a WAV audio file source: "
	 << env->getResultMsg() << "\n";
    exit(1);
  }

  // Get attributes of the audio source:
  unsigned char const bitsPerSample = pcmSource->bitsPerSample();
  if (bitsPerSample != 8 && bitsPerSample !=  16) {
    *env << "The input file contains " << bitsPerSample
	 << " bit-per-sample audio, which we don't handle\n";
    exit(1);
  }
  sessionState.source = pcmSource;
  unsigned const samplingFrequency = pcmSource->samplingFrequency();
  unsigned char const numChannels = pcmSource->numChannels();
  unsigned bitsPerSecond
    = samplingFrequency*bitsPerSample*numChannels;
  *env << "Audio source parameters:\n\t" << samplingFrequency << " Hz, ";
  *env << bitsPerSample << " bits-per-sample, ";
  *env << numChannels << " channels => ";
  *env << bitsPerSecond << " bits-per-second\n";

  // Add in any filter necessary to transform the data prior to streaming.
  // (This is where any audio compression would get added.)
  char const* mimeType;
  unsigned char payloadFormatCode;
  if (bitsPerSample == 16) {
#ifdef CONVERT_TO_ULAW
    // Add a filter that converts from raw 16-bit PCM audio (in little-endian order)
    // to 8-bit u-law audio:
    sessionState.source
      = uLawFromPCMAudioSource::createNew(*env, pcmSource, 1/*little-endian*/);
    if (sessionState.source == NULL) {
      *env << "Unable to create a u-law filter from the PCM audio source: "
	   << env->getResultMsg() << "\n";
      exit(1);
    }
    bitsPerSecond /= 2;
    mimeType = "PCMU";
    if (samplingFrequency == 8000 && numChannels == 1) {
      payloadFormatCode = 0; // a static RTP payload type
    } else {
      payloadFormatCode = 96; // a dynamic RTP payload type
    }
    *env << "Converting to 8-bit u-law audio for streaming => "
	 << bitsPerSecond << " bits-per-second\n";
#else
    // The 16-bit samples in WAV files are in little-endian order.
    // Add a filter that converts them to network (i.e., big-endian) order:
    sessionState.source = EndianSwap16::createNew(*env, pcmSource);
    if (sessionState.source == NULL) {
      *env << "Unable to create a little->bit-endian order filter from the PCM audio source: "
	   << env->getResultMsg() << "\n";
      exit(1);
    }
    mimeType = "L16";
    if (samplingFrequency == 44100 && numChannels == 2) {
      payloadFormatCode = 10; // a static RTP payload type
    } else if (samplingFrequency == 44100 && numChannels == 1) {
      payloadFormatCode = 11; // a static RTP payload type
    } else {
      payloadFormatCode = 96; // a dynamic RTP payload type
    }
    *env << "Converting to network byte order for streaming\n";
#endif
  } else { // bitsPerSample == 8
    // Don't do any transformation; send the 8-bit PCM data 'as is':
    mimeType = "L8";
    payloadFormatCode = 96; // a dynamic RTP payload type
  }

  // Create 'groupsocks' for RTP and RTCP:
  struct in_addr destinationAddress;
  destinationAddress.s_addr = chooseRandomIPv4SSMAddress(*env);
  // Note: This is a multicast address.  If you wish instead to stream
  // using unicast, then you should use the "testOnDemandRTSPServer"
  // test program - not this test program - as a model.

  const unsigned short rtpPortNum = 2222;
  const unsigned short rtcpPortNum = rtpPortNum+1;
  const unsigned char ttl = 255;

  const Port rtpPort(rtpPortNum);
  const Port rtcpPort(rtcpPortNum);

  sessionState.rtpGroupsock
    = new Groupsock(*env, destinationAddress, rtpPort, ttl);
  sessionState.rtpGroupsock->multicastSendOnly(); // we're a SSM source
  sessionState.rtcpGroupsock
    = new Groupsock(*env, destinationAddress, rtcpPort, ttl);
  sessionState.rtcpGroupsock->multicastSendOnly(); // we're a SSM source

  // Create an appropriate audio RTP sink (using "SimpleRTPSink")
  // from the RTP 'groupsock':
  sessionState.sink
    = SimpleRTPSink::createNew(*env, sessionState.rtpGroupsock,
			       payloadFormatCode, samplingFrequency,
			       "audio", mimeType, numChannels);

  // Create (and start) a 'RTCP instance' for this RTP sink:
  const unsigned estimatedSessionBandwidth = bitsPerSecond/1000;
      // in kbps; for RTCP b/w share
  const unsigned maxCNAMElen = 100;
  unsigned char CNAME[maxCNAMElen+1];
  gethostname((char*)CNAME, maxCNAMElen);
  CNAME[maxCNAMElen] = '\0'; // just in case
  sessionState.rtcpInstance
    = RTCPInstance::createNew(*env, sessionState.rtcpGroupsock,
			      estimatedSessionBandwidth, CNAME,
			      sessionState.sink, NULL /* we're a server */,
			      True /* we're a SSM source*/);
  // Note: This starts RTCP running automatically

  // Create and start a RTSP server to serve this stream:
  sessionState.rtspServer = RTSPServer::createNew(*env, 8554);
  if (sessionState.rtspServer == NULL) {
    *env << "Failed to create RTSP server: " << env->getResultMsg() << "\n";
    exit(1);
  }
  ServerMediaSession* sms
    = ServerMediaSession::createNew(*env, "testStream", inputFileName,
	   "Session streamed by \"testWAVAudiotreamer\"", True/*SSM*/);
  sms->addSubsession(PassiveServerMediaSubsession::createNew(*sessionState.sink, sessionState.rtcpInstance));
  sessionState.rtspServer->addServerMediaSession(sms);

  char* url = sessionState.rtspServer->rtspURL(sms);
  *env << "Play this stream using the URL \"" << url << "\"\n";
  delete[] url;

  // Finally, start the streaming:
  *env << "Beginning streaming...\n";
  sessionState.sink->startPlaying(*sessionState.source, afterPlaying, NULL);
}


void afterPlaying(void* /*clientData*/) {
  *env << "...done streaming\n";

  // End by closing the media:
  Medium::close(sessionState.rtspServer);
  Medium::close(sessionState.rtcpInstance);
  Medium::close(sessionState.sink);
  delete sessionState.rtpGroupsock;
  Medium::close(sessionState.source);
  delete sessionState.rtcpGroupsock;

  // We're done:
  exit(0);
}
