package com.nativium.app.helper

import android.content.Context
import android.content.res.Resources
import android.graphics.PorterDuff
import android.graphics.drawable.Drawable
import android.view.View
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.content.res.AppCompatResources
import androidx.core.content.ContextCompat
import com.nativium.app.R
import kotlin.math.roundToInt

object UIHelper {

    fun showAlert(context: Context, title: String, message: String) {
        val alertDialog = AlertDialog.Builder(context).create()
        alertDialog.setTitle(title)
        alertDialog.setMessage(message)

        alertDialog.setButton(
            AlertDialog.BUTTON_NEUTRAL,
            context.getString(R.string.dialog_button_ok)
        ) { dialog, _ -> dialog.dismiss() }

        alertDialog.show()
    }

    fun showViewById(container: View?, viewId: Int) {
        if (container == null) {
            return
        }

        val view = container.findViewById<View>(viewId)

        if (view != null) {
            view.visibility = View.VISIBLE
        }
    }

    fun hideViewById(container: View?, viewId: Int) {
        if (container == null) {
            return
        }

        val view = container.findViewById<View>(viewId)

        if (view != null) {
            view.visibility = View.GONE
        }
    }

    fun convertDpToPixel(dp: Float): Float {
        val metrics = Resources.getSystem().displayMetrics
        val px = dp * (metrics.densityDpi / 160f)
        return px.roundToInt().toFloat()
    }

    fun drawableColorChange(context: Context, icon: Int, color: Int): Drawable? {
        val drawable = AppCompatResources.getDrawable(context, icon)
        drawable?.setColorFilter(ContextCompat.getColor(context, color), PorterDuff.Mode.SRC_IN)

        return drawable
    }
}
