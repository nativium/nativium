package com.nativium.app.ui.activity

import android.content.Intent
import com.nativium.app.ui.activity.base.BaseActivity
import com.nativium.app.ui.fragment.MainFragment
import com.nativium.app.ui.fragment.base.BaseFragment

class MainActivity : BaseActivity() {
    private var fragment: MainFragment? = null

    override val fragmentInstance: BaseFragment?
        get() {
            fragment = MainFragment.newInstance()
            return fragment
        }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        fragment?.onActivityResult(requestCode, resultCode, data)
    }
}
