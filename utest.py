

import unittest
import vkData
from datetime import datetime
class Test(unittest.TestCase):
    """
    Класс тестирования методов класса vkbot.
    """
    def test_insert(self):
        """
        Проверяет запрос insert.
        """
        clas=vkData.vkbot()
        ans,c,conn = clas.insert(1,datetime.now())
        self.assertEqual(ans, True)
        
    def test_select(self):
        """
        Проверяет запрос select.
        """
        clas=vkData.vkbot()
        ans = clas.select()
        ans = isinstance(ans,list)
        self.assertEqual(ans, True)
        
if __name__ == '__main__':
    unittest.main()
