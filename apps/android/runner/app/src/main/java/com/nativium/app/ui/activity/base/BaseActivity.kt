package com.nativium.app.ui.activity.base

import android.os.Bundle
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import com.nativium.app.R
import com.nativium.app.ui.fragment.base.BaseFragment

open class BaseActivity : AppCompatActivity() {
    protected open val fragmentInstance: BaseFragment?
        get() = null

    protected val activityLayout: Int
        get() = R.layout.activity_base

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(activityLayout)
        setContentFragment()
        createAll()
    }

    protected fun createAll() {
        // ignore
    }

    protected fun setContentFragment() {
        val fm = supportFragmentManager
        val ft = fm.beginTransaction()

        fragmentInstance?.let {
            ft.replace(R.id.fragmentContent, it)
        }

        ft.commit()
    }

    protected fun onHomeButtonSelected() {
        finish()
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == android.R.id.home) {
            onHomeButtonSelected()
        }

        return super.onOptionsItemSelected(item)
    }
}
