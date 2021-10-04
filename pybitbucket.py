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
            A dictionary containing the keys:
            - key: str, the build key
            - description: str, build description (optional)
            - url: str, build url (optional)
            - refname: str, build reference name (optional)
            - state: str, build status (optional)
            - created_on: str, when this build was created (optional)
            - updated_on: str, when this build was updated (optional)
            - type: str, build type (optional)
            - name: str, build name (optional)
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
    """Class representing a commit on Bitbucket"""

    def __init__(self, commit_data):
        """

        :param commit_data: dict
            A dictionary containing:
            - hash: str, commit id sha256
            - date: str, commit date (optional)
            - message: str, commit message (optional)
            - type: str, commit type (optional)
        """

        assert 'hash' in commit_data
        self.hash = commit_data.get('hash')
        self.date = commit_data.get('date')
        self.message = commit_data.get('message')
        self.type = commit_data.get('type')


def get_values(config, api_url):
    """
    A wrapper for the API get request
    :param config: dict
        The application configurations
    :param api_url: str
        The API URL
    :return: list
        List of objects returned by the API request
    """

    logging.debug(f'API URL: {api_url}')
    credentials = Credentials(config)

    response = requests.get(api_url, auth=credentials.tuple)
    if not response.ok:
        logging.error(f'Error: {response.status_code}')
        return []

    contents = response.content.decode('utf-8')
    return json.loads(contents).get('values', [])


def get_build_status(config):
    """

    :param config: dict
        The application configurations
    :return: list of BuildStatus
    """

    api_url = ApiCommit(config).api_url + '/statuses'
    return [BuildStatus(value) for value in get_values(config, api_url)]


def get_commits(config):
    """

    :param config: dict
        The application configurations
    :return: list of Commit
    """

    api_url = ApiRepositories(config).api_url + '/commits'
    return [Commit(value) for value in get_values(config, api_url)]


def load_config(arguments):
    """
    Load configuration from config file and/or from program arguments
    :param arguments: dict
        Program arguments
    :return: dict with configurations
    """

    config = {}

    if arguments.config:
        config = json.load(arguments.config)
    
    if arguments.user:
        config['username'] = arguments.user

    if arguments.password:
        config['password'] = arguments.password

    if arguments.revision:
        config['revision'] = arguments.revision

    if arguments.repository:
        config['repository'] = arguments.repository

    if arguments.owner:
        config['owner'] = arguments.owner

    logging.info(f"Running {arguments.cmd} with configuration:")
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

    objects = globals()[args.cmd](load_config(args))
    for obj in objects:
        print(obj.csv(' | '))
