#!/usr/bin/env python3

import requests
import logging
import json
import argparse

from credentials import Credentials
from api_interfaces import ApiCommit, ApiRepositories


class BitbucketObject:

    def csv(self, separator=','):
        attributes = self.__dict__
        return separator.join([str(attributes.get(key)) for key in attributes.keys()])

    def table(self):
        return self.csv(' | ')


class BuildStatus(BitbucketObject):

    def __init__(self, build_status):
        """

        :param build_status: dict
        """
        assert 'key' in build_status

        self.key = build_status.get('key')
        self.description = build_status.get('description', '')
        self.url = build_status.get('url', '')
        self.refname = build_status.get('refname', '')
        self.state = build_status.get('state', '')
        self.created_on = build_status.get('created_on', '')
        self.updated_on = build_status.get('updated_on', '')
        self.type = build_status.get('type', '')
        self.name = build_status.get('name', ' ')

        # TODO: add repository, links, commit object.


class Commit(BitbucketObject):

    def __init__(self, commit_data):
        assert 'hash' in commit_data
        self.hash = commit_data.get('hash')
        self.date = commit_data.get('date')
        self.message = commit_data.get('message')
        self.type = commit_data.get('type')


def get_values(config, api_url):
    logging.debug(f'API URL: {api_url}')
    credentials = Credentials(config)

    response = requests.get(api_url, auth=credentials.tuple)
    if not response.ok:
        logging.error(f'Error: {response.status_code}')
        return []

    contents = response.content.decode('utf-8')
    return json.loads(contents).get('values', [])


def get_build_status(config):
    api_url = ApiCommit(config).api_url + '/statuses'
    return [BuildStatus(value) for value in get_values(config, api_url)]


def get_commits(config):
    api_url = ApiRepositories(config).api_url + '/commits'
    return [Commit(value) for value in get_values(config, api_url)]


def load_config(args):

    config = {}

    if args.config:
        config = json.load(args.config)
    
    if args.user:
        config['username'] = args.user

    if args.password:
        config['password'] = args.password

    if args.revision:
        config['revision'] = args.revision

    if args.repository:
        config['repository'] = args.repository

    if args.owner:
        config['owner'] = args.owner

    logging.info(f"Running {args.cmd} with configuration:")
    for key in config.keys():
        logging.debug(f"    {key}: {config[key]}")

    return config


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    args_parser = argparse.ArgumentParser(description='A Python implementation of Bitbucket API')
    
    args_parser.add_argument('cmd', choices=['get_build_status', 'get_commits'], action='store')
    args_parser.add_argument('--revision', help='Commit hash', type=str)
    args_parser.add_argument('--user', help='Bitbucket username', type=str)
    args_parser.add_argument('--password', help='Bitbucket password', type=str)
    args_parser.add_argument('--repository', help='Bitbucket repository name', type=str)
    args_parser.add_argument('--owner', help='Bitbucket repository owner', type=str)
    args_parser.add_argument('--config', help='Read arguments from file', type=argparse.FileType('r'))
    
    args = args_parser.parse_args()

    objs = globals()[args.cmd](load_config(args))
    for obj in objs:
        print(obj.csv( ' | '))
