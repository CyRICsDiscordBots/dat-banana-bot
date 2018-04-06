import discord
import sys
import os
import io
import asyncio
import json
import ezjson
from discord.ext import commands


class mod:
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def dm(self, ctx, user: discord.Member, *, msg: str):
        """Escort your DM to someone thru the bot. Usage: *dm [tag person] [msg]"""
        try:
            await user.send(msg)
            await ctx.message.delete()            
            await ctx.send("SuccESS! Your DM has made it! :white_check_mark: ")
        except commands.MissingPermissions:
            await ctx.send("Aw, come on! You thought you could get away with DM'ing people without permissions.")
        except:
            await ctx.send("Error :x:. Make sure your message is shaped in this way: *dm [tag person] [msg]")


    
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        """It's time to stop. Sends that warning. Usage: *warn [tag person] [reason]"""
        try:
            color = discord.Color(value=0xf44242)
            em = discord.Embed(color=color, title=f"WARNING: by {ctx.message.author.name} from **{ctx.author.guild.name}**.", description=f"{reason}")
            await user.send(embed=em)
            await ctx.message.delete()
            await ctx.send("User has been DM'd :white_check_mark:. Pray that the user is a gud boi now. :pray:")
        except discord.ext.commands.MissingPermissions:
            await ctx.send("Aw, come on! You thought you could get away with warning people without permissions.")
        except:
            await ctx.send("Something happened and the DM could not make it :x:. The user could be blocking DMs from the server, or you did not use the format correctly. Usage: *warn [tag person] [reason].")    
       
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, num: int):
        """Deletes a # of msgs. *purge [# of msgs].""" 
        try: 
            if num is None:
                await ctx.send("How many messages would you like me to delete? Usage: *purge [number of msgs]")
            else:
                try:
                    float(num)
                except ValueError:
                    return await ctx.send("The number is invalid. Make sure it is valid! Usage: *purge [number of msgs]")
                await ctx.channel.purge(limit=num+1)
                msg = await ctx.send("Purged successfully :white_check_mark:", delete_after=3)
        except discord.Forbidden:
            await ctx.send("Purge unsuccessful. The bot does not have Manage Msgs permission.")
        except commands.errors.MissingPermissions:
            await ctx.send("Aw, come on! You thought you could get away with purging without permissions.")
    
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member = None, *, reason=None):
        """Kicks a member into the world outside your server."""
        if user is None:
            await ctx.send("To boot the member, use the command like this: \n*kick [@user] [reason]")
        try:
            await user.kick(reason=reason)
            color = discord.Color(value=0x00ff00)
            em = discord.Embed(color=color, title='Kicked!')
            em.add_field(name='User', value=user.name)
            em.add_field(name='Kicked By', value=ctx.author.name)
            if reason is None:
                reason = 'No reason given.'
            else:
                reason = reason
            em.add_field(name='Reason', value=reason)
            em.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send("Oops! I don't have enough permissions to use the boot.")
        except commands.errors.MissingPermissions:
            await ctx.send("Nice try. You need `Kick Members` Permission to use this!")
        
        
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member = None, msgdeletedays: int = 0, *, reason=None):
        """Swings the mighty Ban Hammer on that bad boy."""
        if user is None:
            await ctx.send("To swing the ban hammer, use the command like this: \n*ban [@user] [days of msgs to delete] [reason]")
        try:
            await user.ban(delete_message_days=msgdeletedays, reason=reason)
            color = discord.Color(value=0x00ff00)
            em = discord.Embed(color=color, title='Banned!')
            em.add_field(name='User', value=user.name)
            em.add_field(name='Banned By', value=ctx.author.name)
            em.add_field(name='Days of Messages Deleted', value=f"{msgdeletedays} days")
            if reason is None:
                reason = 'No reason given.'
            else:
                reason = reason
            em.add_field(name='Reason', value=reason)
            em.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send("Oops! I don't have enough permissions to swing this ban hammer.")
        except commands.errors.MissingPermissions:
            await ctx.send("Nice try. You need `Ban Members` Permissions to use this!")



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, user: discord.Member, mutetime=None):
        '''Forces someone to shut up. Usage: *mute [user] [time in mins]'''
        try:
            if mutetime is None:
                await ctx.channel.set_permissions(user, send_messages=False)
                await ctx.send(f"{user.mention} is now forced to shut up. :zipper_mouth: ")
            else:
                try:
                    mutetime =int(mutetime)
                    mutetime = mutetime * 60
                except ValueError:
                    return await ctx.send("Your time is an invalid number. Make sure...it is a number.")
                await ctx.channel.set_permissions(user, send_messages=False)
                await ctx.channel.send(f"{user.mention} is now forced to shut up. :zipper_mouth: ")
                await asyncio.sleep(mutetime)
                await ctx.channel.set_permissions(user, send_messages=True)
                await ctx.channel.send(f"{user.mention} is now un-shutted up.")
        except discord.Forbidden:
            return await ctx.send("I could not mute the user. Make sure I have the manage channels permission.")
        except commands.errors.MissingPermissions:
            await ctx.send("Aw, come on! You thought you could get away with shutting someone up without permissions.")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def servermute(self, ctx, user: discord.Member = None):
        '''Forces someone to shut up through the entire server. OUCH.'''
        if user is None:
            await ctx.send("Bruh. Tag a user to mute them...")
        else:
            msg = await ctx.send("Muting user...")
            try:
                lol = discord.utils.get(ctx.guild.roles, name='Muted')
                await user.add_roles(lol)
            except:
                try:
                    role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(permissions=68420672)) 
                    # Given permissions: Change nickname, read messages, use external emojis, add reactions, 
                    # voice: view channel, voice: connect. EVERYTHING ELSE IS DISABLED.
                    await user.add_roles(role)
                except discord.Forbidden:
                    return await msg.edit(content="Don't have enough permissions. For flawless bot functions, give the Administrator permission to the bot.")
            await msg.edit(content="The user has been muted for this server. :zipper_mouth:")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def serverunmute(self, ctx, user: discord.Member = None):
        '''Un-shuts someone up from the entire server. YEEE.'''
        if user is None:
            await ctx.send("Bruh. Tag a user to unmute them...")
        else:
            msg = await ctx.send("Unmuting user...")
            try:
                await user.remove_roles("Muted")
            except discord.Forbidden:
                return await ctx.send("Uh-oh! Not enough permissions!")
            await msg.edit(content="The user has been unmuted for this server. :grin:")



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Allows someone to un-shut up. Usage: *unmute [user]'''
        try:
            await ctx.channel.set_permissions(user, send_messages=True)
            await ctx.channel.send(f"{user.mention} is now un-shutted up.")
        except discord.Forbidden:
            await ctx.send("Couldn't unmute the user. Uh-oh...")
        except commands.errors.MissingPermissions:
            await ctx.send("Aw, come on! You thought you could get away with shutting someone up without permissions.")              
    

    @commands.command(aliases=['welcome'])
    async def welcomemsg(self, ctx, action=None):
        if action is None:
            em = discord.Embed(color=discord.Color(value=0x00ff00), title='Welcome Messages')
            try:
                f = open("data/welcomemsg.json").read()
                x = json.loads(f)
                if x[str(ctx.guild.id)] is False:
                    em.description = 'Welcome messages are disabled for this server.'
                else:
                    em.description = f'Welcome messages are turned on for this server, set in <#{x[str(ctx.guild.id)]}>.'
            except KeyError:
                em.description = 'Welcome messages are disabled for this server.'
            await ctx.send(embed=em)
        else:
            if action.lower() == 'on':
                await ctx.send("Please mention the channel to set welcome messages in.")
                try:
                    x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
                except asyncio.TimeoutError:
                    return await ctx.send("Request timed out. Please try again.")
                if not x.content.startswith("<#") and not x.content.endswith(">"):
                    return await ctx.send("Please properly mention the channel.")
                channel = x.content.strip("<#").strip(">")
                try:
                    channel = int(channel)
                except ValueError:
                    return await ctx.send("Did you properly mention a channel? Probably not.")
                ezjson.dump("data/welcomemsg.json", ctx.guild.id, channel)
                await ctx.send("Successfully turned on welcome messages for this guild.")
            elif action.lower() == 'off':
                ezjson.dump("data/welcomemsg.json", ctx.guild.id, False)
                await ctx.send("Successfully turned off welcome messages for this guild.")


    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def modlog(self, ctx, action=None):
        if action is None:
            f = open("data/modlog.json").read()
            x = json.loads(f)
            em = discord.Embed(color=discord.Color(value=0x00ff00), title="Mod Log Status")
            try:
                x[str(ctx.guild.id)]
                em.description = f'Mod logs are enabled in this server, in <#{x[str(ctx.guild.id)]}>.'
            except KeyError:
                em.description = 'Mod logs are turned off for this server.'
            return await ctx.send(embed=em)
        if action.lower() == 'on':
            await ctx.send("Please mention the channel for mod logs to be sent in.")
            try:
                x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out. Please try again.")
            if not x.content.startswith("<#") and not x.content.endswith(">"):
                return await ctx.send("Please properly mention the channel.")
            channel = x.content.strip("<#").strip(">")
            try:
                channel = int(channel)
            except ValueError:
                return await ctx.send("Did you properly mention a channel? Probably not.")
            ezjson.dump("data/modlog.json", ctx.guild.id, channel)
            return await ctx.send(f"Successfully turned on Mod Logs in <#{channel}>. Enjoy! :white_check_mark:")
        if action.lower() == 'off':
            ezjson.dump("data/modlog.json", ctx.guild.id, False)
            return await ctx.send("Turned off Mod Logs. Whew...")
        else:
            return await ctx.send("That ain't an action. Please enter either `on` or `off`.")


    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def prefix(self, ctx, prefix=None):
        em = discord.Embed(color=discord.Color(value=0x00ff00), title="Bot Prefix")
        if prefix is None:
            em.description = f"The bot's prefix for server **{ctx.guild.name}** is set to `{ctx.prefix}`."
            em.set_footer(text="The bot commands can always be accessed by [tag bot] [command].\nUse *prefix clear to remove it.")
            return await ctx.send(embed=em)
        if prefix.lower() == 'clear':
            ezjson.dump("data/prefix.json", ctx.guild.id, "*")
            em.description = f"The bot's prefix is now set to the default: `*`."
            em.set_footer(text="The bot commands can always be accessed by [tag bot] [command].\nUse *prefix clear to remove it.")
            return await ctx.send(embed=em)
        else:
            ezjson.dump("data/prefix.json", ctx.guild.id, prefix)
            em.description = f"The bot's prefix for this server is set to: `{prefix}`."
            em.set_footer(text="The bot commands can always be accessed by [tag bot] [command].\nUse *prefix clear to remove it.")
            return await ctx.send(embed=em)
        
            



        
    # @commands.group(invoke_without_command = True)
    # @commands.has_permissions(administrator = True)
    # async def banword(self, ctx, word=None):
    #     '''Command group that allows you to add/delete banned words for your server.'''
    #     em = discord.Embed(color=discord.Color(value=0x00ff00), title='Banned Words')
    #     em.description = ''
    #     try:
    #         f = open("data/guildconfig.json").read()
    #         x = json.loads(f)
    #         for i in x[str(ctx.guild.id)]["censoredWords"]:
    #             em.description += f"{i[word]} \n"
    #         await ctx.send(embed=em)
    #     except:
    #         em.description = "You have not added any ban words for this guild."
    #         return await ctx.send(embed=em)




    # @banword.command()
    # async def add(self, ctx, *, word=None):
    #     '''Adds a word to the ban list'''
    #     if word is None:
    #         await ctx.send("Please enter a word to add it to the censor.")
    #     else:
    #         f = open("data/guildconfig.json").read()
    #         x = json.loads(f)
    #         x[ctx.guild.id] = {
    #             "censoredWords":[word]
    #         }
    #         y = open("data/guildconfig.json","w")
    #         y.write(json.dumps(x, indent=4))
    #         try:
    #             await ctx.message.delete()
    #         except discord.Forbidden:
    #             pass
    #         await ctx.send("Success. The word has been added to the censor. :white_check_mark:")


    # @banword.command()
    # async def remove(self, ctx, *, word=None):
    #     '''Removes a word from the ban list.'''
    #     if word is None:
    #         await ctx.send("Please enter a word to remove it from the censor.")
    #     else:
    #         f = open("data/guildconfig.json").read()
    #         x = json.loads(f)
    #         try:
    #             e = open("data/guildconfig.json", "w")
    #             j = json.loads(e)
    #             wordlist = j[str(ctx.guild.id)]['censoredWords']
    #             wordlist.remove(word)
    #             await ctx.send("Done. Removed the word from the ban list.")
    #         except KeyError:
    #             await ctx.send("The word was not found in the ban list.")
        

    # @commands.group()
    # async def welcomemsg(self, ctx):
    #     '''Enables/disables welcome messages for this guild.'''
    #     em = discord.Embed(color=discord.Color(value=0x00ff00), title='Welcome Messages')
    #     try:
    #         f = open(f"data/welcome/{ctx.guild.id}.json").read()
    #         x = json.loads(f)
    #         em.description = f"Your current welcome message is set to: \n{x['message']['msg']}"
    #     except:
    #         em.description = "No welcome message found for the guild. \n\n**How to Use:**\n`*welcome on`: Turns on welcome messages.\n`*welcome off`: Turns off welcome messages."
    #         return await ctx.send(embed=em)
        

    # @welcomemsg.command()
    # async def on(self, ctx):
    #     await ctx.send("Enabling welcome messages. Ready for takeoff!", delete_after=3)
    #     await asyncio.sleep(3)
    #     await ctx.send("Which channel would you like the messages to be sent in? Mention the channel.")
    #     try:
    #         x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)        
    #         if not x.content.startswith("<#") and not x.content.endswith(">"):
    #             return await ctx.send("Invalid channel provided. Please mention a valid channel.")
    #     except asyncio.TimeoutError:
    #         return await ctx.send("The request timed out. Please try again.")
    #     await ctx.send(f"The channel {x.content} has been set.")
    #     await ctx.send("Please enter the message you want to display. \n\n```Variables: \n{name}: The name of the member.\n{mention}: Tag the memebr.\n{membercount}: The number of members in the guild. \n{guild}: The guild's name.```")
    #     try:
    #         f = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=90.0)
    #     except asyncio.TimeoutError:
    #         return await ctx.send("The request timed out. Please try again.")
    #     await ctx.send("Your message has been set.")
    #     await asyncio.sleep(1)
    #     msg = await ctx.send("Please wait while we load your data...")
    #     a = open(f"data/welcome/{ctx.guild.id}.json", "w")
    #     data = {
    #         "msg": f.content,
    #         "channel": x.content.strip("<").strip("#").strip(">")
    #     }
    #     b = json.load(a)
    #     b.write(json.dumps(ctx.guild.id, data, indent=4)
    #     await ctx.send("Successfully set welcome messages! :yum:   ")




def setup(bot): 
    bot.add_cog(mod(bot))        
