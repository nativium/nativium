package com.nativium.app.adapter

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter
import com.nativium.app.ui.fragment.base.BaseFragment

open class MainViewPagerAdapter(fragmentActivity: FragmentActivity) :
    FragmentStateAdapter(fragmentActivity) {

    private var fragmentList: ArrayList<Fragment>? = null

    init {
        this.fragmentList = ArrayList()
    }

    fun add(fragment: BaseFragment) {
        fragmentList?.add(fragment)
    }

    override fun getItemCount(): Int {
        return fragmentList?.size ?: 0
    }

    override fun createFragment(position: Int): Fragment {
        return fragmentList?.get(position) ?: Fragment()
    }
}
