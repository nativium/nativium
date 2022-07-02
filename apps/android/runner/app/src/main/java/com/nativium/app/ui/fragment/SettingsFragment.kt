package com.nativium.app.ui.fragment

import android.view.View
import androidx.lifecycle.MutableLiveData
import com.nativium.app.BuildConfig
import com.nativium.app.R
import com.nativium.app.adapter.SimpleOptionAdapter
import com.nativium.app.enumerator.LoadStateEnum
import com.nativium.app.enumerator.SimpleOptionTypeEnum
import com.nativium.app.helper.UIHelper
import com.nativium.app.model.SimpleOption
import com.nativium.app.ui.fragment.base.BaseListFragment
import com.nativium.core.ApplicationCore
import java.util.Locale

class SettingsFragment :
    BaseListFragment<SimpleOption>(),
    SimpleOptionAdapter.SimpleOptionAdapterListener {

    override val screenNameForAnalytics: String
        get() = "Settings"

    override fun createAll(view: View) {
        super.createAll(view)

        setupToolbar(R.string.title_settings)
        createLiveData()
    }

    override fun onLoadNewData() {
        super.onLoadNewData()

        val list = ArrayList<SimpleOption>()
        list.add(SimpleOption(SimpleOptionTypeEnum.APP_VERSION))

        listData?.value = list

        remoteDataLoadState = LoadStateEnum.LOADED
    }

    private fun createLiveData() {
        listData = MutableLiveData()

        (listData as MutableLiveData<ArrayList<SimpleOption>>).observe(
            this
        ) { list ->
            adapter = SimpleOptionAdapter(requireContext(), list)
            (adapter as SimpleOptionAdapter).setListener(this)

            updateAdapter()

            adapter.notifyDataSetChanged()
        }
    }

    override fun needLoadNewData(): Boolean {
        return true
    }

    override fun onSimpleOptionItemClick(view: View, option: SimpleOption) {
        when {
            option.type == SimpleOptionTypeEnum.APP_VERSION -> doActionAppVersion()
        }
    }

    private fun doActionAppVersion() {
        try {
            context?.let { context ->
                val version = String.format(
                    Locale.getDefault(),
                    "Library: %s\nVersion: %s\nBuild: %d",
                    ApplicationCore.shared().version,
                    BuildConfig.VERSION_NAME,
                    BuildConfig.VERSION_CODE
                )

                UIHelper.showAlert(context, getString(R.string.dialog_title), version)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    companion object {
        fun newInstance(): SettingsFragment {
            return SettingsFragment()
        }
    }
}
