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
// A common framework, used for the "openRTSP" and "playSIP" applications
// Interfaces

#include "liveMedia.hh"

extern Medium* createClient(UsageEnvironment& env, int verbosityLevel,
			    char const* applicationName);

extern char* getOptionsResponse(Medium* client, char const* url,
				char* username, char* password);

extern char* getSDPDescriptionFromURL(Medium* client, char const* url,
				      char const* username,
				      char const* password,
				      char const* proxyServerName,
				      unsigned short proxyServerPortNum,
				      unsigned short clientStartPortNum);

extern Boolean clientSetupSubsession(Medium* client,
				     MediaSubsession* subsession,
				     Boolean streamUsingTCP);

extern Boolean clientStartPlayingSession(Medium* client,
					 MediaSession* session);

extern Boolean clientTearDownSession(Medium* client,
				     MediaSession* session);

extern Boolean allowProxyServers;
extern Boolean controlConnectionUsesTCP;
extern Boolean supportCodecSelection;
extern char const* clientProtocolName;
extern unsigned statusCode;
