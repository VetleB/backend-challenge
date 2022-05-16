import click
import re
import requests


class IpAddress(click.ParamType):
    name = 'ip'

    def convert(self, value, param, ctx):
        valid = re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$', value)

        if not valid:
            self.fail(f'{value} is not an IPv4 address + port number', param, ctx)

        return value


@click.group()
@click.argument('ip',
                type=IpAddress())
@click.pass_context
def main(ctx, ip):
    ctx.obj = {
        'ip': ip
    }


@main.command()
@click.pass_context
def info(ctx):
    ip = ctx.obj['ip']
    r = requests.get('http://{}/datasets'.format(ip))
    data = r.json()['file_info']
    for ft in data:
        click.echo('{} - {} MB'.format(ft[0], '{:.1f}'.format(ft[1]/1000)))


@main.command()
@click.option('--source', '-s',
              type=click.Path(),
              help='Path to source file')
@click.pass_context
def create(ctx):
    ip = ctx.obj['ip']
    r = requests.post('http://{}/datasets'.format(ip))
    click.echo("")


@main.command()
@click.argument('id')
@click.option('--dest', '-d',
              type=click.Path(),
              help='Path to file destination')
@click.pass_context
def get(ctx, id, dest):
    ip = ctx.obj['ip']
    r = requests.get('http://{}/datasets/{}'.format(ip, id))
    sc = r.status_code

    if dest:
        with open(dest, 'w') as f:
            f.write(r.text)
        click.echo(sc)
    else:
        if r.status_code == 200:
            click.echo(sc)
        else:
            click.echo(sc)


@main.command()
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    ip = ctx.obj['ip']
    r = requests.delete('http://{}/datasets/{}'.format(ip, id))
    click.echo(r.status_code)


@main.command()
@click.argument('id')
@click.pass_context
def excel(ctx, id):
    ip = ctx.obj['ip']
    click.echo("")


if __name__ == '__main__':
    main()
