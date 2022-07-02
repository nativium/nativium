package com.nativium.app.ui.fragment

import android.view.View
import androidx.lifecycle.MutableLiveData
import com.nativium.app.R
import com.nativium.app.adapter.SimpleOptionAdapter
import com.nativium.app.enumerator.LoadStateEnum
import com.nativium.app.enumerator.SimpleOptionTypeEnum
import com.nativium.app.helper.UIHelper
import com.nativium.app.model.SimpleOption
import com.nativium.app.ui.fragment.base.BaseListFragment
import com.nativium.core.ApplicationCore
import kotlin.random.Random

class HomeFragment :
    BaseListFragment<SimpleOption>(),
    SimpleOptionAdapter.SimpleOptionAdapterListener {

    override val screenNameForAnalytics: String
        get() = "Home"

    override fun createAll(view: View) {
        super.createAll(view)

        setupToolbar(R.string.title_home)
        createLiveData()
        validateLoadData()
    }

    override fun onLoadNewData() {
        super.onLoadNewData()

        val list = ArrayList<SimpleOption>()
        list.add(SimpleOption(SimpleOptionTypeEnum.MULTIPLY))

        listData?.value = list

        remoteDataLoadState = LoadStateEnum.LOADED
    }

    override fun onSimpleOptionItemClick(view: View, option: SimpleOption) {
        when (option.type) {
            SimpleOptionTypeEnum.MULTIPLY -> {
                doActionMultiply()
            }
            else -> {
                // ignore
            }
        }
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
        return isAdded
    }

    private fun doActionMultiply() {
        context?.let { context ->
            UIHelper.showAlert(
                context,
                getString(R.string.dialog_title),
                getString(
                    R.string.dialog_message_result,
                    ApplicationCore.shared()
                        .multiply(Random.nextDouble(1.0, 100.0), Random.nextDouble(1.0, 100.0))
                        .toString()
                )
            )
        }
    }

    companion object {
        fun newInstance(): HomeFragment {
            return HomeFragment()
        }
    }
}
