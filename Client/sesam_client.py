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
                type=IpAddress(),
                help='Ip address and port for querying')
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
    click.echo(r.status_code)
    click.echo(r.text)


@main.command()
@click.pass_context
def create(ctx):
    ip = ctx.obj['ip']
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

    if dest:
        with open(dest, 'w') as f:
            f.write(r.text)
    else:
        click.echo(r.text)


@main.command()
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    ip = ctx.obj['ip']
    click.echo("")


@main.command()
@click.argument('id')
@click.pass_context
def excel(ctx, id):
    ip = ctx.obj['ip']
    click.echo("")


if __name__ == '__main__':
    main()
