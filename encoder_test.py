from encoder import encoder #include encoder.py


enc = encoder("192.168.88.252","m0dts","xxxxx")    #setup new encoder instance - IP of encoder,stream name, stream key
#enc.restartUDP()   #UDP is normally enabled by the Pluto but can need re-starting
enc.set_streaming_source()
enc.streaming("SD")
enc.streaming("OFF")
enc.streaming("HD")

enc.create_osd_image("M0DTS",64)
enc.upload_osd_image(0,"image.jpg")     #MainStream
enc.disable_osd_image(0)
enc.enable_osd_image(0,15,15,64)

#enc.create_osd_image("M0DTS",48)
#enc.upload_osd_image(1,"image.jpg")    #SubStream
#enc.disable_osd_image(1)
#enc.enable_osd_image(1,15,15,64)
