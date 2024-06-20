# class Dog:
#     attr1 = "mammal"
    
#     def __init__(self, name):
#         self.name = name

#     def speak(self):
#         print("my Name is {}".format(self.name))
    

#     pass



# Rodger = Dog("Rodger")
# Tommy = Dog("Tommy")

# print("Roger is a {}".format(Rodger.__class__.attr1))

# print("Tommy is a {}".format(Tommy.__class__.attr1))

# # print("my name is {}".format(Rodger.name))
# # print("my name is {}".format(Tommy.name))

# Rodger.speak()


# class GFG:

#     env = "work"
#     def __init__(self, name, company):
#         self.name = name
#         self.company = company

#     def show(self):
#         print("Hello, my name is {}".format(self.name)+ " and I work in {}".format(self.company))


# obj = GFG("Mahdis", "seneca")

# print(obj)
# obj.show()



# class car:
#     def __init__(self, model, color):
#         self.model = model
#         self.color = color
    
#     def show(self):
#         print("The Model is ", self.model)
#         print("The Color is ", self.color)

# audi = car("audi", "Black")
# honda = car("Honda", "White")

# audi.show()
# honda.show()

# print("model for audi is ", audi.model)
# print("the color for honda is ", honda.color)



# class A:
#     def __init__(self,sth):
#         print("A init called")
#         self.sth = sth


# class B(A):
#     def __init__(self,sth):
#         A.__init__(self, sth)
#         print("B init called")
#         self.sth = sth


# obj = B("something")

# li = ['a', 'b', 'v']

# for i in li:
#     if i == 'a':
#         pass
#     else:
#         print(i)




# class person():
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id

#     # def get_name(self):
#     #     return self.name
    
#     # def is_employee(self):
#     #     return False
#     def display(self):
#         print(self.name)
#         print(self.id)


# class emp(person):
#     def __init__(self,  name, id, salary, post):
#         self.salary = salary
#         self.post = post

#         super().__init__("Rahil", id)
#     # def print(self):
#         # print("Emp class called")

#     # def is_employee(self):
#     #     return True
#     def displayInfo(self):
#         print(self.salary, self.post)

# emp_details = emp("Mahdis", 22, 2020, "devops")
# # emp_details.display()

# emp_details.display()
# emp_details.displayInfo()
# # print(emp_details.get_name())
# # print(emp_details.is_employee())



# class Base1():
#     str0 = "Greek0"
#     def __init__(self):
#         self.str1 = "Greek1"
#         print("base1")

# class Base2():
#     def __init__(self):
#         self.str2 = "greek2"
#         print("base2")

# class Derived(Base1, Base2):
#     def __init__(self):
#         Base1.__init__(self)
#         Base2.__init__(self)
#         print("Dervied")

#     def printStr(self):
#         print(self.str0, self.str1, self.str2)

# obj = Derived()
# obj.printStr()


# class Base():
#     type = "friut"
#     def __init__(self, name):
#         self.name = name

#     def get_name(self):
#         return self.name
    
# class Child(Base):
#     def __init__(self, name, age):
#         Base.__init__(self, name)
#         self.age = age

#     def get_age(self):
#         return self.age
    
# class GrandChild(Child):
#     def __init__(self, name, age, address):
#         Child.__init__(self, name, age)
#         self.address = address

#     def get_address(self):
#         return self.address
    
# g = GrandChild("Mahdis", 12, "Canada")
# print(g.get_name(), g.get_age(), g.get_address())
# c = GrandChild("apple",18, "CANADA")
# print(getattr(c, "type"))

# class C():
#     def __init__(self):
#         self.c = 21

#         self.__d = 42

# class D(C):
#     def __init__(self):
#         self.e = 84
#         C.__init__(self)

# obj = D()
# print(obj.c)
# print(obj.__D)

# class Base:
#     def __init__(self):
#         self.__a = 2
#         print(self.__a)

# class Derived(Base):
#     def __init__(self):
#         Base.__init__(self)
#         print("Calling protected memebr of base calss: ", self.__a)
        
        # self.__a = 3
        # print("Calling modified memebr of base calss: ", self.__a) 

# obj1 = Derived()
# obj2 = Base()

# print(obj2._Base__a)
# print("accessing protected memeber of obj1", obj1.__a)
# print("accessing protected memeber of obj2", obj2.__a)


# class base:
#     def __init__(self, name=None):
#         if name is None:
#             print("Default constructor called")
#         else:
#             self.name = name
#             print("Parameterized constructore called with name", self.name)

#     def method(self):
#         if hasattr(self, 'name'):
#             print("method called with name", self.name)
#         else:
#             print("Method called without name")

# obj1 = base()

# obj1.method()

# obj2 = base("John")
# obj2.method()

# def permutation(string, step = ''):
#     if len(string) == 0:
#         print("this is " + step)
#     for i in range(len(string)):
#         print(i)
#         print("next round")
#         newMutation = step + string[i]
#         newString = string[0:i] + string[i+1:]
#         permutation(newString, newMutation)

# text = "ABC"
# print("Permutations of \"" + text + "\" is as below,")
# permutation(text)

# text = "Mahdis"
# reserved_string = ''
# for i in text:
#     reserved_string = i + reserved_string
    

# print(reserved_string)

# print(text[::1])


# a, b = 1, 2
# a , b = b, a
# print("using syntaxt a is ",a , "b is ", b)


# a,b = 1, 2
# a = a + b
# b = a - b 
# a = a - b


# def fib(n):
#     if n <= 1:
#         return n
#     return (fib(n-1)+ fib(n-2))


# num = 3

# for i in range(num):
#     print(fib(i))

# def sum(sample):
#     total = 0
#     for i in str(sample):
#         total += int(i)
#     return total
    



# n = 2021
# print(sum(n))


# def palidrome(text):
#     if text[::-1] == text:
#         print("it's palindrome")
#     else:
#         print("not palindrome")

# sample = "RADAR"
# palidrome(sample)


# def fac(n):
#     if n == 1:
#         return 1
#     else:
#         return (n * fac(n-1))



# sample = 10
# print(fac(sample))


# import os,re

# def write_data(source, destination):
#     if not os.path.isdir(destination):
#         os.mkdir(destination, 666)

#     for file in os.listdir(source):
#         if re.search("File.*txt", file):
#             with open(source+'/'+file,'r') as f, open(destination+'/'+file,'a') as s:
#                 for line in f:
#                     s.write(line)

# write_data('FolderA','FolderC')
# write_data('FolderB','FolderC')


# def find(n):
#     largest = n[0]
#     for i in nums:
#         if largest < i:
#             largest = i
#     return largest


# nums = [1, 5, 8, 6]
# print(find(nums))

# def count_frequency(num):
#     total = {}
#     for i in num:
#         if i in total:
#             total[i] += 1
#         else:
#             total[i] = 1
#     return total


# nums = [1, 2, 3, 2, 1, 3, 2, 4, 5, 4]
# print(count_frequency(nums))

# def is_prime(num):
#     if num < 2:
#         return False
#     for i in range(2, num):
#         if num % i == 0:
#             return False
#     return True

# num = 10
# print(is_prime(num))


# def common(list1, list2):
#     common = []
#     for i in list1:
#         if i in list2:
#             common.append(i)
#     return common

# list_a = [1, 2, 3, 4, 5]
# list_b = [4, 5, 6, 7, 8]
# print(common(list_a, list_b))

# def bubble_sort(num):
#     n = len(num)
#     for i in range(n):
#         for j in range(0, n - i - 1):
#             if num[j] > num[j+1]:
#                 num[j], num[j+1] = num[j+1], num[j]

#         print(num)
#     print("hi" + str(num))



# nums = [5, 2, 8, 1, 9]
# bubble_sort(nums)
# print(nums)



# def find_second_largest(numbers):
#     largest = float('-inf')
#     second_largest = float('-inf')
#     for num in numbers:
#         if num > largest:
#             second_largest = largest
#             largest = num
#         elif num > second_largest and num != largest:
#             second_largest = num
#     return second_largest

# # Test the function
# nums = [10, 5, 8, 20, 3]
# second_largest_num = find_second_largest(nums)
# print(f"The second largest number is {second_largest_num}")



def remove_duplicate(num):
    new_list = []
    for i in num:
        if i not in new_list:
            new_list.append(i)
    return(new_list)



my_list = [1, 2, 3, 2, 1, 3, 2, 4, 5, 4]
print(remove_duplicate(my_list))