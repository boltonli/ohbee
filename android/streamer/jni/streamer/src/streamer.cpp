#include "ob_android_Stream.h"
#include "config.h"
#include "AMRAudioFileDescriptorSource.hh"

#include <liveMedia.hh>
#include <BasicUsageEnvironment.hh>
#include <UsageEnvironment.hh>

extern "C"
{
	#include <jnix.h>
}

Boolean awaitConfigInfo(RTPSink *sink);
void play();

static char doneFlag = 0;
UsageEnvironment *uenv;
MPEG4VideoStreamFramer *videoSource;
AMRAudioFileDescriptorSource *audioSource;
RTPSink *rtpVideoSink;
RTPSink *rtpAudioSink;
FILE* videoFile;
FILE* audioFile;

void Java_ob_android_Stream_stream(JNIEnv *env, jobject obj)
{
	jclass streamClazz = env->GetObjectClass(obj);
	if(streamClazz == NULL)
		return;

	jobject videoPipe, audioPipe;
	if(!getObjectField(env, obj, "video", "Ljnix/Pipe;", &videoPipe))
		return;
	if(!getObjectField(env, obj, "audio", "Ljnix/Pipe;", &audioPipe))
		return;

	jobject videoInputFD, audioInputFD;
	if(!getObjectField(env, videoPipe, "input", "Ljava/io/FileDescriptor;", &videoInputFD))
		return;
	if(!getObjectField(env, audioPipe, "input", "Ljava/io/FileDescriptor;", &audioInputFD))
		return;

	jint vfd, afd;
	if(!getIntField(env, videoInputFD, "descriptor", &vfd))
		return;
	if(!getIntField(env, audioInputFD, "descriptor", &afd))
		return;

	if((videoFile = fdopen(vfd, "rb")) == NULL)
	{
		throwException(env, "java/lang/RuntimeException", "Unable to open the video pipe as a file");
		return;
	}
	logDebug("Video file descriptor opened as a file");
	if((audioFile = fdopen(afd, "rb")) == NULL)
	{
		throwException(env, "java/lang/RuntimeException", "Unable to open the video pipe as a file");
		return;
	}
	logDebug("Audio file descriptor opened as a file");

	logDebug("Starting to stream");
	BasicTaskScheduler* scheduler = BasicTaskScheduler::createNew();
	logDebug("Loaded scheduler");
	uenv = BasicUsageEnvironment::createNew(*scheduler);
	logDebug("Loaded environment");
	DarwinInjector* injector = DarwinInjector::createNew(*uenv, "streamer");
	logDebug("Loaded Darwin injector");

	struct in_addr dummyDestAddress;
	dummyDestAddress.s_addr = 0;
	Groupsock rtpGroupsockVideo(*uenv, dummyDestAddress, 0, 0);
	Groupsock rtcpGroupsockVideo(*uenv, dummyDestAddress, 0, 0);
	Groupsock rtpGroupsockAudio(*uenv, dummyDestAddress, 0, 0);
	Groupsock rtcpGroupsockAudio(*uenv, dummyDestAddress, 0, 0);
	logDebug("Created group sockets");

	// Create an 'MPEG-4 Video RTP' sink from the RTP 'groupsock':
	rtpVideoSink = MPEG4ESVideoRTPSink::createNew(*uenv, &rtpGroupsockVideo, 96);
	rtpAudioSink = AMRAudioRTPSink::createNew(*uenv, &rtpGroupsockVideo, 97);

	logDebug("Created a video sink");
	logDebug("Created an audio sink");

	logDebug("Beginning to play");
	play();

	if(!awaitConfigInfo(rtpVideoSink))
	{
		*uenv << "Failed to get MPEG-4 'config' information from input file: "
			 << uenv->getResultMsg() << "\n";
	    exit(1);
	}

	// Create (and start) a 'RTCP instance' for this RTP sink:
	const unsigned estimatedSessionBandwidthVideo = 200; // in kbps; for RTCP b/w share
	const unsigned maxCNAMElen = 100;
	unsigned char CNAME[maxCNAMElen+1];
	gethostname((char*)CNAME, maxCNAMElen);
	CNAME[maxCNAMElen] = '\0'; // just in case
	logDebug((const char*)CNAME);
	RTCPInstance* videoRTCP =
			RTCPInstance::createNew(*uenv, &rtcpGroupsockVideo,
					estimatedSessionBandwidthVideo, CNAME,
					rtpVideoSink, NULL /* we're a server */);
	RTCPInstance* audioRTCP =
				RTCPInstance::createNew(*uenv, &rtcpGroupsockAudio,
						estimatedSessionBandwidthVideo, CNAME,
						rtpAudioSink, NULL /* we're a server */);
	// Note: This starts RTCP running automatically
	// Add these to our 'Darwin injector':
	injector->addStream(rtpVideoSink, videoRTCP);
	injector->addStream(rtpAudioSink, audioRTCP);
	if(!injector->setDestination(
			"192.168.1.100",
			"hero.sdp",
			"herosession",
			"",
			554,
			"broadcast",
			"broadcast"))
	{
		*uenv << "injector->setDestination() failed: " << uenv->getResultMsg() << "\n";
		exit(1);
	}

	*uenv << "Play this stream (from the Darwin Streaming Server) using the URL:\n"
		<< "\trtsp://" << "localhost" << "/" << "test.sdp" << "\n";
		uenv->taskScheduler().doEventLoop();
}

void afterPlaying(void* clientData)
{
	logDebug("...done reading from file");
	Medium::close(videoSource);
}

void play()
{
	// Open the input file as a 'byte-stream file source':
	ByteStreamFileSource* videoFileSource
			= ByteStreamFileSource::createNew(*uenv, videoFile);
	if(videoFileSource == NULL)
	{
		logError("Unable to open video file");
		exit(1);
	}

	FramedSource* videoES = videoFileSource;
	// Create a framer for the Video Elementary Stream:
	videoSource = MPEG4VideoStreamFramer::createNew(*uenv, videoES);
	audioSource = AMRAudioFileDescriptorSource::createNew(*uenv, audioFile);
	// Finally, start playing:
	logDebug("Beginning to read from file...");
	rtpVideoSink->startPlaying(*videoSource, afterPlaying, rtpVideoSink);
	rtpAudioSink->startPlaying(*audioSource, afterPlaying, rtpAudioSink);
}

static void checkForAuxSDPLine(void* clientData)
{
	RTPSink* sink = (RTPSink*)clientData;
	if (sink->auxSDPLine() != NULL)
	{
		// Signal the event loop that we're done:
		doneFlag = ~0;
	}
	else
	{
		// No luck yet.  Try again, after a brief delay:
		int uSecsToDelay = 100000; // 100 ms
		uenv->taskScheduler().scheduleDelayedTask(uSecsToDelay, (TaskFunc*)checkForAuxSDPLine, sink);
	}
}

Boolean awaitConfigInfo(RTPSink* sink)
{
	// Check whether the sink's 'auxSDPLine()' is ready:
	checkForAuxSDPLine(sink);
	uenv->taskScheduler().doEventLoop(&doneFlag);
	char const* auxSDPLine = sink->auxSDPLine();
	return auxSDPLine != NULL;
}
