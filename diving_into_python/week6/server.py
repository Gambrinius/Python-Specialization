# -*- coding: utf-8 -*-

import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host=host, port=port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class CachedMetrics:
    def __init__(self):
        self.cached_metrics = {}
        self.wrong_resp = 'error\nwrong command\n\n'
        self.ok_resp = 'ok\n\n'

    def get(self, body):
        if len(body.split()) != 1:
            resp = self.wrong_resp
        else:
            metric = body.split()[0]
            if metric in self.cached_metrics:
                metric_resp = ''
                for value_tuple in self.cached_metrics[metric]:
                    value, timestamp = value_tuple
                    metric_resp += f'{metric} {value} {timestamp}\n'
                resp = f'ok\n{metric_resp}\n'
            elif metric == '*':
                metric_resp = ''
                for metric, tuple_list in self.cached_metrics.items():
                    for value_tuple in tuple_list:
                        value, timestamp = value_tuple
                        metric_resp += f'{metric} {value} {timestamp}\n'
                resp = f'ok\n{metric_resp}\n'
            else:
                resp = self.ok_resp
        return resp

    def put(self, body):
        metric, value, timestamp = body.split()
        if metric not in self.cached_metrics:
            self.cached_metrics[metric] = [(float(value), int(timestamp))]
        else:
            # check for existing timestamp
            is_exist = False
            for idx, payload in enumerate(self.cached_metrics[metric]):
                exist_value, exist_timestamp = payload
                if int(timestamp) == exist_timestamp:
                    self.cached_metrics[metric][idx] = (float(value), int(timestamp))
                    is_exist = True
                    break
            # new value, timestamp
            if not is_exist:
                self.cached_metrics[metric].append((float(value), int(timestamp)))
        return self.ok_resp

    def process_data(self, request_data):
        try:
            command, body = request_data.split(' ', 1)
            if command == 'get':
                resp = self.get(body)
            elif command == 'put':
                resp = self.put(body)
            else:
                resp = self.wrong_resp
        except (ValueError, UnicodeDecodeError, IndexError):
            resp = self.wrong_resp
        return resp


class ClientServerProtocol(asyncio.Protocol):
    cached_metrics = CachedMetrics()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.cached_metrics.process_data(data.decode())
        self.transport.write(resp.encode())


if __name__ == "__main__":  # delete when sending the module for verification
    run_server("127.0.0.1", 8888)
