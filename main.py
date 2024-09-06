class Singleton:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, value):
        if not self._initialized:
            self.value = value
            self._initialized = True

# Tạo instance đầu tiên
singleton1 = Singleton(10)
print(singleton1.value)  # Output: 10

# Tạo instance thứ hai
singleton2 = Singleton(30)
print(singleton2.value)  # Output: 10

# Kiểm tra xem cả hai instance có giống nhau không
print(singleton1 is singleton2)  # Output: True
