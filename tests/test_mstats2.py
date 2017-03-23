import unittest
from unittest import TestCase

from ping import MStats2


class Mstats2Test(TestCase):
    def setUp(self):
        self.ms = MStats2()

    def test_init(self):
        self.assertIsInstance(self.ms._this_ip, str)
        self.assertEqual(self.ms._this_ip, '0.0.0.0')

        self.assertIsInstance(self.ms._timing_list, list)
        self.assertEqual(self.ms._timing_list, [])

        self.assertIsInstance(self.ms._packets_sent, int)
        self.assertEqual(self.ms._packets_sent, 0)

        self.assertIsInstance(self.ms._packets_rcvd, int)
        self.assertEqual(self.ms._packets_rcvd, 0)

        # Statistics
        self.assertIsInstance(self.ms._total_time, type(None))
        self.assertIsInstance(self.ms._mean_time, type(None))
        self.assertIsInstance(self.ms._median_time, type(None))
        self.assertIsInstance(self.ms._pstdev_time, type(None))
        self.assertIsInstance(self.ms._frac_loss, type(None))

    def test_get_thisIP(self):
        self.assertEqual(self.ms.thisIP, self.ms._this_ip)

    def test_set_thisIP(self):
        self.ms.thisIP = '127.0.0.1'
        self.assertEqual(self.ms.thisIP, '127.0.0.1')

    def test_get_pktsSent(self):
        self.assertEqual(self.ms.pktsSent, self.ms._packets_sent)

    def test_get_pktsRcvd(self):
        self.assertEqual(self.ms.pktsRcvd, self.ms._packets_rcvd)

    def test_get_pktsLost(self):
        self.assertEqual(self.ms.pktsLost,
                         self.ms._packets_sent - self.ms._packets_rcvd)

    def test_get_minTime(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        self.assertEqual(self.ms.minTime, 1)

    def test_get_maxTime(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        self.assertEqual(self.ms.maxTime, 3)

    def test_get_totTime(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        self.assertEqual(self.ms.totTime, 6)

    def test__get_mean_time(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        mean_time = 6 / 3

        self.assertEqual(self.ms._get_mean_time(), mean_time)
        self.assertEqual(self.ms.mean_time, self.ms._get_mean_time())
        self.assertEqual(self.ms.avrgTime, self.ms._get_mean_time())

    def test_get_median_time(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        median = sorted(self.ms._timing_list)[len(self.ms._timing_list)//2]

        self.assertEqual(self.ms._calc_median_time(), median)

        self.assertEqual(self.ms.median_time, median)

    def test_get_pstdev_time(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        # tests _calc_sum_square_time
        sum_square = self.ms._calc_sum_square_time()
        self.assertEqual(sum_square, 2)

        # tests _calc_pstdev_time
        pstdev = self.ms._calc_pstdev_time()
        self.assertEqual(pstdev, 0.816496580927726)

        # ensures pstdev_time
        self.assertEqual(self.ms.pstdev_time, pstdev)

    def test_get_fracLoss(self):
        self.ms._packets_sent += 1

        loss = self.ms.pktsLost / self.ms.pktsSent

        self.assertEqual(self.ms.fracLoss, loss)

    def test_packet_sent(self):
        self.ms.packet_sent(2)
        self.assertEqual(self.ms.pktsSent, 2)

    def test_packet_received(self):
        self.ms.packet_received(2)
        self.assertEqual(self.ms.pktsRcvd, 2)

    def test_record_time(self):
        self.ms.record_time(1)
        self.assertEqual(len(self.ms._timing_list), 1)

    def test__reset_statistics(self):
        self.ms._reset_statistics()

        self.assertEqual(self.ms._total_time, None)
        self.assertEqual(self.ms._mean_time, None)
        self.assertEqual(self.ms._median_time, None)
        self.assertEqual(self.ms._pstdev_time, None)
        self.assertEqual(self.ms._frac_loss, None)

    def test_calc_median_time(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        median = sorted(self.ms._timing_list)[len(self.ms._timing_list) // 2]

        self.assertEqual(self.ms._calc_median_time(), median)

    def test__calc_sum_square_time(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        sum_square = self.ms._calc_sum_square_time()
        self.assertEqual(sum_square, 2)

    def test__calc_pstdev_time(self):
        self.ms._timing_list.append(1)
        self.ms._timing_list.append(2)
        self.ms._timing_list.append(3)

        pstdev = self.ms._calc_pstdev_time()
        self.assertEqual(pstdev, 0.816496580927726)


if __name__ == '__main__':
    unittest.main()
