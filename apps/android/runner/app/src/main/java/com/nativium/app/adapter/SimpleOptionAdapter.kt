package com.nativium.app.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.nativium.app.R
import com.nativium.app.model.SimpleOption

class SimpleOptionAdapter(
    private val context: Context,
    private val listData: ArrayList<SimpleOption>?
) : RecyclerView.Adapter<SimpleOptionAdapter.ViewHolder>() {

    private var listener: SimpleOptionAdapterListener? = null

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val inflater = LayoutInflater.from(context)
        val view = inflater.inflate(R.layout.list_item_simple_option, parent, false)

        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        listData?.let { listData ->
            val option = listData[position]

            holder.tvTitle.text = option.getDescription(context)

            holder.ivIcon.setImageResource(option.getImage())
            holder.ivIcon.setColorFilter(
                ContextCompat.getColor(
                    context,
                    R.color.list_item_icon_color
                )
            )
        }
    }

    override fun getItemCount(): Int {
        return listData?.size ?: 0
    }

    fun setListener(listener: SimpleOptionAdapterListener) {
        this.listener = listener
    }

    interface SimpleOptionAdapterListener {
        fun onSimpleOptionItemClick(view: View, option: SimpleOption)
    }

    inner class ViewHolder(itemView: View) :
        RecyclerView.ViewHolder(itemView),
        View.OnClickListener {

        val tvTitle: TextView = itemView.findViewById(R.id.tv_title)
        val ivIcon: ImageView = itemView.findViewById(R.id.iv_icon)

        init {
            itemView.setOnClickListener(this)
        }

        override fun onClick(view: View) {
            listener?.onSimpleOptionItemClick(view, listData!![adapterPosition])
        }
    }
}
