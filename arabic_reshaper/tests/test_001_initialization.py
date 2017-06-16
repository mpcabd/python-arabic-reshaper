from __future__ import unicode_literals

import unittest
import arabic_reshaper


class TestDefaultConfiguration(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper()

    def test_configuration_exists(self):
        self.assertIsNotNone(self.reshaper.configuration)

    def test_language(self):
        self.assertIn('language', self.reshaper.configuration)
        self.assertIsNotNone(self.reshaper.configuration['language'])
        self.assertTrue(self.reshaper.configuration['language'])

    def test_support_ligatures(self):
        self.assertIn('support_ligatures', self.reshaper.configuration)
        self.assertIsNotNone(
            self.reshaper.configuration.getboolean('support_ligatures')
        )

    def test_delete_harakat(self):
        self.assertIn('delete_harakat', self.reshaper.configuration)
        self.assertIsNotNone(
            self.reshaper.configuration.getboolean('delete_harakat')
        )

    def test_ligatures(self):
        import arabic_reshaper.ligatures
        for ligature in arabic_reshaper.ligatures.LIGATURES:
            if hasattr(self, 'subTest'):
                with self.subTest(ligature=ligature[0]):
                    self.assertIn(ligature[0], self.reshaper.configuration)
                    self.assertIsNotNone(
                        self.reshaper.configuration.getboolean(ligature[0])
                    )
            else:
                self.assertIn(ligature[0], self.reshaper.configuration)
                self.assertIsNotNone(
                    self.reshaper.configuration.getboolean(ligature[0])
                )

if __name__ == '__main__':
    unittest.main()
