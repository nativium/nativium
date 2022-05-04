package com.nativium.app

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.nativium.core.ApplicationCore
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Instrumented test, which will execute on an Android device.
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
@RunWith(AndroidJUnit4::class)
class CoreInstrumentedTest {

    @Test
    fun useAppContext() {
        // Context of the app under test.
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("com.nativium.app", appContext.packageName)
    }

    @Test
    fun version() {
        val version = ApplicationCore.shared().version
        val versionName = version.split(" ")[0]
        assertEquals(versionName, "1.0.0")
    }

    @Test
    fun multiply() {
        val result = ApplicationCore.shared().multiply(3.0, 4.0)
        assertEquals(result, 12.0, 0.0)
    }
}
