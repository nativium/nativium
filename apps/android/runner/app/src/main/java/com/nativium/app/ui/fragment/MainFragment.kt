package com.nativium.app.ui.fragment

import android.graphics.drawable.ColorDrawable
import android.view.MenuItem
import android.view.View
import androidx.core.content.ContextCompat
import androidx.viewpager2.widget.ViewPager2
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.nativium.app.R
import com.nativium.app.adapter.MainViewPagerAdapter
import com.nativium.app.ui.fragment.base.BaseFragment

class MainFragment : BaseFragment(), BottomNavigationView.OnNavigationItemSelectedListener {

    private var viewPager: ViewPager2? = null
    private var adapter: MainViewPagerAdapter? = null

    private var homeFragment: HomeFragment? = null
    private var settingsFragment: SettingsFragment? = null

    private var navigation: BottomNavigationView? = null

    override val fragmentLayout: Int
        get() = R.layout.fragment_main

    override fun createAll(view: View) {
        super.createAll(view)

        // view pager
        adapter = MainViewPagerAdapter(requireActivity())

        homeFragment = HomeFragment.newInstance()
        adapter?.add(homeFragment!!)

        settingsFragment = SettingsFragment.newInstance()
        adapter?.add(settingsFragment!!)

        // view pager
        viewPager = view.findViewById(R.id.main_view_pager)

        viewPager?.let { viewPager ->
            viewPager.offscreenPageLimit = adapter?.itemCount ?: 0
            viewPager.adapter = adapter
            viewPager.isUserInputEnabled = false
        }

        // bottom navigation
        context?.let { context ->
            navigation = view.findViewById(R.id.navigation)

            navigation?.let { navigation ->
                navigation.background =
                    ColorDrawable(ContextCompat.getColor(context, R.color.white))

                navigation.setOnNavigationItemSelectedListener(this)
            }
        }
    }

    override fun onNavigationItemSelected(item: MenuItem): Boolean {
        homeFragment?.userVisibleHint = false
        settingsFragment?.userVisibleHint = false

        when (item.itemId) {
            R.id.navigation_home -> {
                viewPager?.currentItem = 0
                homeFragment?.userVisibleHint = true
                return true
            }

            R.id.navigation_settings -> {
                viewPager?.currentItem = 1
                settingsFragment?.userVisibleHint = true
                return true
            }
        }

        return false
    }

    companion object {
        fun newInstance(): MainFragment {
            return MainFragment()
        }
    }
}
