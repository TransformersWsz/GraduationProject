package com.wsz;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

public class Main {
    public static class TokenizerMapper extends Mapper<Object, Text, FloatWritable, IntWritable> {

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String str = value.toString();
            String[] arr = str.split("--->");

            float keyOutput = Float.parseFloat(arr[1]);
            int valueOutput = Integer.parseInt(arr[0]);

            context.write(new FloatWritable(keyOutput), new IntWritable(valueOutput));
        }
    }

    // 自定义键比较器
    public static class FloatDescSort extends WritableComparator {

        public FloatDescSort() {
            super(IntWritable.class, true);
        }

        @Override
        public int compare(byte[] arg0, int arg1, int arg2, byte[] arg3, int arg4, int arg5) {
            return -super.compare(arg0, arg1, arg2, arg3, arg4, arg5);//注意使用负号来完成降序
        }

        @Override
        public int compare(Object a, Object b) {
            return -super.compare(a, b);//注意使用负号来完成降序
        }

    }


    public static class IntSumReducer extends Reducer<FloatWritable, IntWritable, IntWritable, FloatWritable> {

        public void reduce(FloatWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            for (IntWritable val : values) {
                context.write(val, key);
//                if (context.getCounter("Counter", "Top").getValue() < 10) {
//                    context.write(val, key);
//                    context.getCounter("Counter", "Top").increment(1);
//                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.set("mapred.textoutputformat.ignoreseparator", "true");
        conf.set("mapred.textoutputformat.separator", "--->");

        Job job = new Job(conf, "interest person");

        job.setJarByClass(Main.class);

        job.setMapperClass(TokenizerMapper.class);
        job.setMapOutputKeyClass(FloatWritable.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(FloatWritable.class);

        job.setSortComparatorClass(FloatDescSort.class);


        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

