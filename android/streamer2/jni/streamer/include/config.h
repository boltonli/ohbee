#include <android/log.h>

#define LOG_TAG "streamer"

#define logFatal(message) androidLog(ANDROID_LOG_FATAL, LOG_TAG, message)
#define logError(message) androidLog(ANDROID_LOG_ERROR, LOG_TAG, message)
#define logWarn(message) androidLog(ANDROID_LOG_WARN, LOG_TAG, message)
#define logInfo(message) androidLog(ANDROID_LOG_INFO, LOG_TAG, message)
#define logDebug(message) androidLog(ANDROID_LOG_DEBUG, LOG_TAG, message)
#define logVerbose(message) androidLog(ANDROID_LOG_VERBOSE, LOG_TAG, message)

#define androidLog(level, tag, message) __android_log_write(level, tag, message)
