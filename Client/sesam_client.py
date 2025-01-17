import json
import re

import click
import requests


class IpAddress(click.ParamType):
    name = 'ip'

    def convert(self, value, param, ctx):
        # Regex that matches on IPv4 addresses with port number
        valid = re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]{1,5}$', value)

        if not valid:
            self.fail(f'{value} is not a valid IPv4 address + port number', param, ctx)

        return value


@click.group()
@click.argument('ip', type=IpAddress())
@click.pass_context
def main(ctx, ip):
    ctx.obj = {
        'ip': ip
    }


@main.command()
@click.pass_context
def info(ctx):
    """
    list the ids of the uploaded datasets and their corresponding file sizes

    :param ctx:
    :return:
    """
    ip = ctx.obj['ip']
    r = requests.get('http://{}/datasets'.format(ip))
    sc = r.status_code

    if sc == 200:
        data = r.json()['file_info']
        for ft in data:
            click.echo('{} - {} MB'.format(ft[0], '{:.1f}'.format(ft[1]/1000)))
    else:
        click.echo(sc)
        click.echo(r.text)


@main.command()
@click.argument('source', type=click.Path())
@click.pass_context
def create(ctx, source):
    """
    Creates a new dataset entry. Takes a JSON file as input, and stores it in the ./dataset folder.

    :param ctx:
    :param source: Path to the file that is to uploaded
    :return: The name of the created dataset entry
    """
    ip = ctx.obj['ip']
    try:
        with open(source, 'r') as f:
            payload = json.load(f)
            r = requests.post('http://{}/datasets'.format(ip), json=payload)
            sc = r.status_code

            if sc != 201:
                click.echo(sc)
            click.echo(r.text)
    except FileNotFoundError:
        click.echo('No file found at {}'.format(source))


@main.command()
@click.argument('id')
@click.argument('dest', type=click.Path())
@click.pass_context
def get(ctx, id, dest):
    """
    Return the dataset entry that matches the id

    :param ctx:
    :param id: id of dataset to be fetched
    :param dest: Path to location where the fetched file is saved
    :return:
    """
    ip = ctx.obj['ip']
    r = requests.get('http://{}/datasets/{}'.format(ip, id))
    sc = r.status_code

    if sc == 200:
        with open(dest, 'w') as f:
            f.write(r.text)
    else:
        click.echo(sc)
        click.echo(r.text)


@main.command()
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """
    Delete the dataset entry that matches the id

    :param ctx:
    :param id: id of dataset to be deleted
    :return:
    """
    ip = ctx.obj['ip']
    r = requests.delete('http://{}/datasets/{}'.format(ip, id))
    sc = r.status_code

    if sc != 204:
        click.echo(r.status_code)
        click.echo(r.text)


@main.command()
@click.argument('id')
@click.argument('dest', type=click.Path())
@click.pass_context
def excel(ctx, id, dest):
    """
    Return the dataset entry that matches the id as a .xls file

    :param ctx:
    :param id: id of dataset to be fetched
    :param dest: Path to location where the fetched file is saved
    :return:
    """
    ip = ctx.obj['ip']
    r = requests.get('http://{}/datasets/{}/excel'.format(ip, id))
    sc = r.status_code

    if sc == 200:
        with open(dest, 'wb') as f:
            f.write(r.content)
    else:
        click.echo(sc)
        print(r.text)


if __name__ == '__main__':
    main()
