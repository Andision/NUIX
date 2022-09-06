package com.example.myapplication.ui.home;

import android.os.Bundle;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.myapplication.R;
import com.example.myapplication.databinding.FragmentHomeBinding;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        HomeViewModel homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textHome;
        homeViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        Button button = root.findViewById(R.id.button_home);
        EditText edittext = root.findViewById(R.id.input_home);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String clip_text = edittext.getText().toString();
                Toast.makeText(getActivity(), "PUSH IS CLICKED, TEXT="+clip_text, Toast.LENGTH_SHORT).show();

//                OkHttpClient client = new OkHttpClient();
//                Request request = new Request.Builder()
//                        .url("http://www.baidu.com")
//                        .build();
//                Response response = client.newCall(request).execute();
//                String responseData = response.body().string();
//                Toast.makeText(getActivity(), responseData, Toast.LENGTH_SHORT).show();




//
                Log.d("response","START HTTP REQUEST");
                OkHttpClient okHttpClient = new OkHttpClient();
                //2.创建Request对象，设置一个url地址（百度地址）,设置请求方式。
                Request request = new Request.Builder().url("http://10.0.2.2:5000/new_clip/"+clip_text).method("GET",null).build();
                //3.创建一个call对象,参数就是Request请求对象
                Call call = okHttpClient.newCall(request);
                //4.请求加入调度，重写回调方法
                call.enqueue(new Callback() {
                    //请求失败执行的方法
                    @Override
                    public void onFailure(Call call, IOException e) {
                        Log.d("response","FAILURE");
                        Looper.prepare();
                        Toast.makeText(getActivity(), "FAILURE", Toast.LENGTH_SHORT).show();
                        Looper.loop();
                    }
                    //请求成功执行的方法
                    @Override
                    public void onResponse(Call call, Response response) throws IOException {
                        String data = response.body().string();
                        Log.d("response",data);
                        Looper.prepare();
                        Toast.makeText(getActivity(), data, Toast.LENGTH_SHORT).show();
                        Looper.loop();
                    }
                });

            }
        });

        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}