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
// A SIP client test program that opens a SIP URL argument,
// and extracts the data from each incoming RTP stream.

#include "playCommon.hh"
#include "SIPClient.hh"

Medium* createClient(UsageEnvironment& env,
                     int verbosityLevel, char const* applicationName) {
  // First, trim any directory prefixes from "applicationName":
  char const* suffix = &applicationName[strlen(applicationName)];
  while (suffix != applicationName) {
    if (*suffix == '/' || *suffix == '\\') {
      applicationName = ++suffix;
      break;
    }
    --suffix;
  }

  extern unsigned char desiredAudioRTPPayloadFormat;
  extern char* mimeSubtype;
  return SIPClient::createNew(env,
			      desiredAudioRTPPayloadFormat, mimeSubtype,
			      verbosityLevel, applicationName);
}

char* getOptionsResponse(Medium* client, char const* url,
			 char* username, char* password) {
  SIPClient* sipClient = (SIPClient*)client;
  sipClient->envir().setResultMsg("NOT SUPPORTED IN CLIENT");//#####
  return NULL;//#####
}

char* getSDPDescriptionFromURL(Medium* client, char const* url,
			       char const* username, char const* password,
			       char const* proxyServerName,
			       unsigned short proxyServerPortNum,
			       unsigned short clientStartPortNum) {
  SIPClient* sipClient = (SIPClient*)client;

  if (proxyServerName != NULL) {
    // Tell the SIP client about the proxy:
    NetAddressList addresses(proxyServerName);
    if (addresses.numAddresses() == 0) {
      client->envir() << "Failed to find network address for \""
		      << proxyServerName << "\"\n";
    } else {
      NetAddress address = *(addresses.firstAddress());
      unsigned proxyServerAddress // later, allow for IPv6 #####
	= *(unsigned*)(address.data());
      if (proxyServerPortNum == 0) proxyServerPortNum = 5060; // default

      sipClient->setProxyServer(proxyServerAddress, proxyServerPortNum);
    }
  }

  if (clientStartPortNum == 0) clientStartPortNum = 8000; // default
  sipClient->setClientStartPortNum(clientStartPortNum);

  char* result;
  if (username != NULL && password != NULL) {
    result = sipClient->inviteWithPassword(url, username, password);
  } else {
    result = sipClient->invite(url);
  }

  return result;
}

Boolean clientSetupSubsession(Medium* client, MediaSubsession* subsession,
			      Boolean streamUsingTCP) {
  subsession->sessionId = "mumble"; // anything that's non-NULL will work
  return True;
}

Boolean clientStartPlayingSession(Medium* client,
				  MediaSession* /*session*/) {
  SIPClient* sipClient = (SIPClient*)client;
  return sipClient->sendACK();
  //##### This isn't quite right, because we should really be allowing
  //##### for the possibility of this ACK getting lost, by retransmitting
  //##### it *each time* we get a 2xx response from the server.
}

Boolean clientTearDownSession(Medium* client,
			      MediaSession* /*session*/) {
  if (client == NULL) return False;
  SIPClient* sipClient = (SIPClient*)client;
  return sipClient->sendBYE();
}

Boolean allowProxyServers = True;
Boolean controlConnectionUsesTCP = False;
Boolean supportCodecSelection = True;
char const* clientProtocolName = "SIP";
