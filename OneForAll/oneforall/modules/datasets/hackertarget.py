from common import utils
from common.query import Query


class HackerTarget(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = self.register(domain)
        self.module = 'Dataset'
        self.source = "HackerTargetQuery"
        self.addr = 'https://api.hackertarget.com/hostsearch/'

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        params = {'q': self.domain}
        resp = self.get(self.addr, params)
        if not resp:
            return
        if resp.status_code == 200:
            subdomains_find = utils.match_subdomain(self.domain, resp.text)
            if subdomains_find:
                # 合并搜索子域名搜索结果
                self.subdomains = self.subdomains.union(subdomains_find)

    def run(self):
        """
        类执行入口
        """
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def do(domain):  # 统一入口名字 方便多线程调用
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = HackerTarget(domain)
    query.run()


if __name__ == '__main__':
    do('example.com')
