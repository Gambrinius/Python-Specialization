import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        try:
            self._socket = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("Cannot create connection", err)

    def _process_metrics(self, content):
        # split response by [metric, value, timestamp]
        data_tuples = [content[i:i+3] for i in range(0, len(content), 3)]

        metric_dict = {}
        for data_tuple in data_tuples:
            metric, value, timestamp = data_tuple
            if metric in metric_dict:
                metric_dict[metric].append((int(timestamp), float(value)))
            else:
                metric_dict[metric] = [(int(timestamp), float(value))]

        for key, tuple_list in metric_dict.items():  # sort values by timestamp
            metric_dict[key] = sorted(tuple_list, key=lambda v: v[0])

        return metric_dict

    def _read(self):
        data = b""

        while not data.endswith(b"\n\n"):
            try:
                data += self._socket.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)

        return data.decode('utf-8')

    def get(self, metric):
        try:
            self._socket.sendall(f'get {metric}\n'.encode('utf-8'))
            response = self._read().split()
            status, content = response[0], response[1:]

            if status != 'ok':
                raise ClientError("Server returns error status")

            metric_dict = self._process_metrics(content)
        except Exception as err:
            raise ClientError('Server returns invalid data', err)

        return metric_dict

    def put(self, metric, value, timestamp=None):
        try:
            timestamp = timestamp or int(time.time())
            self._socket.sendall(f'put {metric} {value} {timestamp}\n'.encode('utf-8'))
            response = self._read().split()
            status, _ = response[0], response[1:]

            if status != 'ok':
                raise ClientError("Server returns error status")

        except socket.error as err:
            raise ClientError(f"Caught exception socket.error: {err.strerror}")

    def close(self):
        try:
            self._socket.close()
        except socket.error as err:
            raise ClientError("Error. Do not close the connection", err)


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=15)
    print(client.get("*"))
