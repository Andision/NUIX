package com.example.myapplication.ui.dashboard;

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

import com.alibaba.fastjson.JSON;
import com.example.myapplication.R;
import com.example.myapplication.databinding.FragmentDashboardBinding;

import java.io.IOException;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class DashboardFragment extends Fragment {

    private FragmentDashboardBinding binding;

    private String saved_encrypt_str;
    private String DEVICE_ID = "Pixel 2";
    private String AES_Decryption(String content, String key){
        return content.substring(0,8);
    }

    private String AES_Encryption(String content, String key){
        return content+"|"+key;
    }

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        DashboardViewModel dashboardViewModel =
                new ViewModelProvider(this).get(DashboardViewModel.class);

        binding = FragmentDashboardBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textDashboard;
        dashboardViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        Button button_pair = root.findViewById(R.id.button_pair);
        button_pair.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getActivity(), "PAIR INIT", Toast.LENGTH_SHORT).show();

                OkHttpClient okHttpClient = new OkHttpClient();
                //2.创建Request对象，设置一个url地址（百度地址）,设置请求方式。
                Request request = new Request.Builder().url("http://192.168.10.93:5000/device_pair_init?device_id="+DEVICE_ID).method("GET",null).build();
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

                        Map<String,String> parseObject = JSON.parseObject(data, Map.class);
                        String code=parseObject.get("code");
                        Log.d("response",code);
                        String encrypt_str=parseObject.get("encrypt_str");
                        Log.d("response",encrypt_str);
                        saved_encrypt_str = encrypt_str;

                        Looper.prepare();
                        Toast.makeText(getActivity(), "code="+code, Toast.LENGTH_SHORT).show();
                        Looper.loop();
                    }
                });

            }
        });

        EditText edittext = root.findViewById(R.id.input_pair);
        Button button_verify = root.findViewById(R.id.button_verify);
        button_verify.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getActivity(), "VERIFY", Toast.LENGTH_SHORT).show();

                String pin = edittext.getText().toString();
                String init_random_int = AES_Decryption(saved_encrypt_str, DEVICE_ID+pin);

                OkHttpClient okHttpClient = new OkHttpClient();
                //2.创建Request对象，设置一个url地址（百度地址）,设置请求方式。
                Request request = new Request.Builder().url("http://192.168.10.93:5000/device_pair_verify?device_id="+DEVICE_ID+"&init_random_int="+init_random_int).method("GET",null).build();
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

                        Map<String,String> parseObject = JSON.parseObject(data, Map.class);
                        String code=parseObject.get("code");
                        Log.d("response",code);

                        Looper.prepare();
                        Toast.makeText(getActivity(), "code="+code, Toast.LENGTH_SHORT).show();
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
