class Config:
    tb_url = "http://210.211.96.129:8088/"
    tb_username = "khanh@rangdong.com.vn"
    tb_password = "123456a@"
    tb_host = "210.211.96.129"
    tb_port = 8088

    num_threads = 1000  # num_devices / num_threads must be an integer

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance