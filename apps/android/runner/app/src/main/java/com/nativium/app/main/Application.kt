package com.nativium.app.main

import android.os.StrictMode
import android.util.Log
import androidx.appcompat.app.AppCompatDelegate
import androidx.multidex.MultiDexApplication
import com.nativium.app.BuildConfig
import com.nativium.app.main.Constants.LOG_GROUP

class Application : MultiDexApplication() {

    override fun onCreate() {
        super.onCreate()

        instance = this

        initializeStrictMode()

        AppCompatDelegate.setCompatVectorFromResourcesEnabled(true)

        loadNativeLibrary()
    }

    override fun onTerminate() {
        Log.d(LOG_GROUP, "[Application : onTerminate] App terminated")
        super.onTerminate()
    }

    private fun loadNativeLibrary() {
        try {
            System.loadLibrary("nativium")
        } catch (e: UnsatisfiedLinkError) {
            Log.e(LOG_GROUP, "Could not load native library: " + e.message)
            e.printStackTrace()
        }
    }

    private fun initializeStrictMode() {
        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(
                StrictMode.ThreadPolicy.Builder()
                    .detectAll()
                    .penaltyLog()
                    .build()
            )

            StrictMode.setVmPolicy(
                StrictMode.VmPolicy.Builder()
                    .detectLeakedSqlLiteObjects()
                    .detectLeakedClosableObjects()
                    .penaltyLog()
                    .build()
            )
        }
    }

    companion object {
        lateinit var instance: Application
            private set
    }
}
