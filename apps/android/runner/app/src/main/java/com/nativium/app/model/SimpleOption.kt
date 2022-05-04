package com.nativium.app.model

import android.content.Context
import com.nativium.app.R
import com.nativium.app.enumerator.SimpleOptionTypeEnum

class SimpleOption(val type: SimpleOptionTypeEnum) {

    fun getDescription(context: Context): String {
        return when {
            type === SimpleOptionTypeEnum.APP_VERSION -> context.getString(R.string.option_app_version)
            type === SimpleOptionTypeEnum.MULTIPLY -> context.getString(R.string.option_multiply)
            else -> ""
        }
    }

    fun getImage(): Int {
        return R.drawable.ic_simple_option
    }
}
