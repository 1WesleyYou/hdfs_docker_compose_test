import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.io.*;

import java.io.*;
import java.net.URI;

public class hdfsUtilFuncs {
    public static void main(String[] args) throws Exception {
        // Configurations for the HDFS
        Configuration conf = new Configuration();
        conf.set("dfs.namenode.file.close.num-committed-allowed", "1");
        conf.setInt("dfs.blockreport.incremental.intervalMsec", 1000);
        conf.set("fs.defaultFS", "hdfs://localhost:8020");
        conf.setInt("dfs.replication", 2);
        conf.setBoolean("dfs.support.append", true);

        FileSystem fs = FileSystem.get(new URI("hdfs://namenode:8020"), conf);

        Path remotePath = new Path("/user/youyuchen/tmp/b.txt");
        Path localPath = new Path("/workspace/java-client/src/main/java/a.txt");
        System.out.println("Uploading file to HDFS...");

        fs.mkdirs(new Path("/user/youyuchen/tmp"));
        System.out.println("Creating the directory /home/youyuchen/");
//        uploadFile(fs, remotePath, localPath);
        bugHdfs17757(fs, remotePath, localPath);
    }

    // inject bugs hdfs-17757
    public static void bugHdfs17757(FileSystem fs_, Path target_path_, Path local_) throws IOException {
        FileSystem fs_local = FileSystem.getLocal(new Configuration());
//        fs_.mkdirs(target_path_.getParent());
        try (FSDataOutputStream out1 = fs_.create(target_path_)) {
            out1.writeUTF("hello1\n");
            out1.close();
        }

        try (FSDataOutputStream out2 = fs_.append(target_path_)) {
            out2.writeUTF("hello2\n");
            out2.close();
        }


    }

    // apis to put file to hdfs
    public static void uploadFile(FileSystem fs_, Path remote_, Path local_) throws IOException {
        FileSystem fs_local = FileSystem.getLocal(new Configuration());
        fs_.mkdirs(remote_.getParent());
        // overwrite the file if it exists
//        System.out.println(remote_);
        System.out.println(local_);
        try (FSDataOutputStream out = fs_.create(remote_); FSDataInputStream in = fs_local.open(local_)) {
            IOUtils.copyBytes(in, out, 4096, false);
            System.out.println("Uploaded file " + remote_ + " to " + local_);
        }
        System.out.println(local_ + " uploaded to " + remote_);
    }

    // apis to download file from hdfs
    public static void downloadFile(FileSystem fs_, Path local_, Path remote_) throws IOException {

    }

    // apis to delete file from hdfs
    public static void deleteFile(FileSystem fs_, Path remote_) throws IOException {
        if (fs_.exists(remote_)) {
            fs_.delete(remote_, true);
            System.out.println(remote_ + " deleted from hdfs");
        } else {
            System.out.println(remote_ + " does not exist in hdfs");
        }
    }

    // apis to append to file in hdfs
    public static void appendFile(FileSystem fs_, Path local_, Path remote_) throws IOException {
        try (FSDataOutputStream out = fs_.append(remote_); FSDataInputStream in = fs_.open(local_)) {
            IOUtils.copyBytes(in, out, 4096, false);
        }
        System.out.println(remote_ + " appended to " + local_);
    }
}
