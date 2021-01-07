async def send_me_message(msg, args):
    await msg.delete()
    if len(args) >= 1:
        if args[0] == 'анон':
            args.pop(0)
            text_string = " ".join(args)
            await msg.channel.send(text_string)
        elif args[0] == 'анонттс':
            args.pop(0)
            text_string = " ".join(args)
            await msg.channel.send(text_string, tts=True)
        else:
            text_string = " ".join(args)
            await msg.channel.send(f'{msg.author.mention} {text_string}')
    else:
        return
