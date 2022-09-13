package com.example.myapplication.ui.notifications;

import android.os.Bundle;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.myapplication.R;
import com.example.myapplication.databinding.FragmentNotificationsBinding;

import java.io.IOException;
import java.util.ArrayList;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class NotificationsFragment extends Fragment {

  private String URL_PREFIX = "http://192.168.10.93:5000";
  private ArrayList s;
  private ArrayAdapter<String> a;
  private ListView listView;

  private FragmentNotificationsBinding binding;

  private class MyThread1 extends Thread {

    private int ticket = 100;//一个窗口有100张票
    private String name; //窗口名, 也即是线程的名字

    public void updateUI() {
      a.notifyDataSetChanged();
      return;
    }

    public MyThread1(String name) {
      this.name = name;
    }

    //在run方法里复写需要进行的操作:卖票速度是1s/张
    @Override
    public void run() {
      while (true) {
//        Log.d("response", "START HTTP REQUEST");
        OkHttpClient okHttpClient = new OkHttpClient();
        //2.创建Request对象，设置一个url地址（百度地址）,设置请求方式。
        Request request = new Request.Builder().url(URL_PREFIX + "/get_data").method("GET", null).build();
        //3.创建一个call对象,参数就是Request请求对象
        Call call = okHttpClient.newCall(request);
        //4.请求加入调度，重写回调方法
        call.enqueue(new Callback() {
          //请求失败执行的方法
          @Override
          public void onFailure(Call call, IOException e) {
//            Log.d("response", "FAILURE");
//            Looper.prepare();
//            Toast.makeText(getActivity(), "FAILURE", Toast.LENGTH_SHORT).show();
//            Looper.loop();
          }

          //请求成功执行的方法
          @Override
          public void onResponse(Call call, Response response) throws IOException {
            String data = response.body().string();
//            Log.d("response", data);
            if (data != "[]") {
              System.out.println(data);
            }


//            listView.setAdapter(new ArrayAdapter(getActivity(), android.R.layout.simple_list_item_1, s));
//            Looper.prepare();
//            Toast.makeText(getActivity(), data, Toast.LENGTH_SHORT).show();
//            Looper.loop();
          }
        });
        try {
          Thread.sleep(2000);
        } catch (InterruptedException e) {
          e.printStackTrace();
        }
      }

    }

  }

  public View onCreateView(@NonNull LayoutInflater inflater,
                           ViewGroup container, Bundle savedInstanceState) {
    NotificationsViewModel notificationsViewModel =
      new ViewModelProvider(this).get(NotificationsViewModel.class);

    binding = FragmentNotificationsBinding.inflate(inflater, container, false);
    View root = binding.getRoot();

    final TextView textView = binding.textNotifications;
    notificationsViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

    s = new ArrayList();
    s.add(0);
    s.add(1);

    listView = root.findViewById(R.id.list_notifications);
    a = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, s);
    listView.setAdapter(a);

    MyThread1 mt1 = new MyThread1("窗口1");
    mt1.start();

    return root;
  }

  @Override
  public void onDestroyView() {
    super.onDestroyView();
    binding = null;
  }
}
