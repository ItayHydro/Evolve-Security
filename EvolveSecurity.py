import discord
from discord.utils import get
from discord.ext import commands
import asyncio
import random

client = commands.Bot(command_prefix = '?')

@client.event
async def on_ready():
    print('EvolveSecurity Online(Checked).')
    return await client.change_presence(activity=discord.Activity(type=3, name='EvolveSecurity | ?help'))

@client.event
async def on_member_join(member):
    print(f'{member} Just joined a server')

@client.event
async def on_member_remove(member):
    print(f'{member} Just left a server')

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    print(f'member has Requested to clear {amount} messages.')
    await ctx.send (f'Successfully cleared {amount} messages.', delete_after = 2)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Missing permissions, you have to be administrator to use this.')

@client.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s user info" .format(user.display_name), description=" ", color= discord.Color(random.randint(0x000000, 0xFFFFFF)))
    embed.add_field(name="name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Account created at", value=user.created_at.strftime("%a, %#d %b %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined server at", value=user.joined_at.strftime("%a, %#d %b %Y, %I:%M %p UTC"))
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Is the user bot", value=user.bot)

    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send( embed = embed)

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    print(f'Successfully banned {member}.')
    await ctx.send(f'Successfully banned {member}.')
    
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Missing permissions, you have to be administrator to use this.')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    print(f'Successfully banned {member}.')
    await ctx.send(f'Successfully banned {member}.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Missing permissions, you have to be administrator to use this.')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Successfully unbanned {user.name}.')
            return
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Missing permissions, you have to be administrator to use this.')

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Please tag a member to mute")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f'{member} has been mute.')
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Missing permissions, you have to be administrator to use this.')

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send('Please tag a member to unmute')
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f'{member} has been unmuted.')

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Missing permissions, you have to be administrator to use this.')


client.run('yourtoken')
