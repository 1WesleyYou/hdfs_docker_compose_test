package com.example.hdfsmetrics;

import com.fasterxml.jackson.databind.ObjectMapper;
import javax.management.MBeanServerConnection;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import java.io.File;
import java.util.HashMap;
import java.util.Map;
import javax.management.openmbean.CompositeData;

public class Exporter {
    public static void main(Stoing[] args) throws Exception {
        // take in 3 arguments: jmx host, port, output file path
        if (args.length < 3) {
            System.err.println("Usage: Exporter <jmxHost> <jmxPort> <outputFile>");
            System.exit(1);
        }
        String host = args[0];
        String port = args[1];
        String outPath = args[2];

        String url = String.format(
            "service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi", host, port);
        JMXConnector jmxc = JMXConnectorFactory.connect(
            new JMXServiceURL(url));
        MBeanServerConnection mbsc = jmxc.getMBeanServerConnection();

        // 例：读取 NameNodeInfo Bean 中的几个字段
        ObjectName bean = new ObjectName(
          "Hadoop:service=NameNode,name=NameNodeInfo");
        CompositeData info = (CompositeData)
          mbsc.getAttribute(bean, "FSNamesystem");

        // 将需要的属性放入 Map
        Map<String,Object> metrics = new HashMap<>();
        for (String key : info.getCompositeType().keySet()) {
            metrics.put(key, info.get(key));
        }

        // 序列化为 JSON
        ObjectMapper mapper = new ObjectMapper();
        mapper.writerWithDefaultPrettyPrinter()
              .writeValue(new File(outPath), metrics);

        jmxc.close();
        System.out.println("Metrics written to " + outPath);
    }
}
