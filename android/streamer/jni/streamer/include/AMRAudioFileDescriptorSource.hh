#ifndef _AMR_AUDIO_FILE_DESCRIPTOR_SOURCE_HH
#define _AMR_AUDIO_FILE_DESCRIPTOR_SOURCE_HH

#ifndef _AMR_AUDIO_FILE_SOURCE_HH
#include "AMRAudioFileSource.hh"
#endif

class AMRAudioFileDescriptorSource: public AMRAudioSource
{
	public:
		static AMRAudioFileDescriptorSource* createNew(UsageEnvironment &env, FILE *file);
	private:
		AMRAudioFileDescriptorSource(UsageEnvironment &env, FILE *file, Boolean isWideband, unsigned numChannels);
		virtual ~AMRAudioFileDescriptorSource();
	private:
		virtual void doGetNextFrame();
	private:
		FILE *fFid;
};
#endif
