import logging
import time
import unittest

import thalesians.pypes as pypes
import thalesians.pypes.zmq as zmq_pypes

class TestPypes(unittest.TestCase):    
    def test_pypes(self):
        outgoing = None
        incoming = None
        try:
            logging.info('Opening outgoing pype')
            outgoing = zmq_pypes.ZMQPype(direction=pypes.Direction.OUTGOING, name="example", port=41822)
            time.sleep(1)
            logging.info('Opening incoming pype')
            incoming = zmq_pypes.ZMQPype(direction=pypes.Direction.INCOMING, name="example", port=41822)
            time.sleep(1)
            self.assertFalse(outgoing.closed)
            self.assertFalse(incoming.closed)
            logging.info('Sending on outgoing pype')
            bytes_sent = outgoing.send(123)
            logging.info(f'Bytes sent: {bytes_sent}')
            self.assertFalse(outgoing.closed)
            self.assertFalse(incoming.closed)
            time.sleep(1)
            logging.info('Receiving on incoming pype')
            value, eof = incoming.receive(notify_of_eof=True)
            self.assertFalse(outgoing.closed)
            self.assertFalse(incoming.closed)
            self.assertEqual(value, 123)
            self.assertFalse(eof)
            self.assertFalse(outgoing.closed)
            self.assertFalse(incoming.closed)
            logging.info('Sending on outgoing pype')
            outgoing.send(456)
            self.assertFalse(outgoing.closed)
            self.assertFalse(incoming.closed)
            logging.info('Closing outgoing pype')
            outgoing.close()
            self.assertTrue(outgoing.closed)
            self.assertFalse(incoming.closed)
            logging.info('Receiving on incoming pype')
            value, eof = incoming.receive(notify_of_eof=True)
            self.assertEqual(value, 456)
            self.assertTrue(eof)
            self.assertTrue(outgoing.closed)
            self.assertTrue(incoming.closed)
            logging.info('All done')
        finally:
            if outgoing and not outgoing.closed:
                outgoing.close
            if incoming and not incoming.closed:
                incoming.close()    


if __name__ == '__main__':
    unittest.main()
