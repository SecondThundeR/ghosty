async def meMessage(msg, args):
    await msg.delete()
    if len(args) >= 1:
        if args[0] == 'анон':
            args.pop(0)
            textString = " ".join(args)
            await msg.channel.send(textString)
        elif args[0] == 'анонттс':
            args.pop(0)
            textString = " ".join(args)
            await msg.channel.send(textString, tts=True)
        else:
            textString = " ".join(args)
            await msg.channel.send(f'{msg.author.mention} {textString}')
    else:
        return
