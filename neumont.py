# Now that we have collected all the Infinity Stones, what will
# happen if we combine them all together?
# To find out, enter the correct answers from the other
# challenges into the following variables.
#
# How will you know you have succeeded?  Trust us... you'll know.
# Your success is.... inevitable!

# The number of letters (no punctuation) in the second word of the message
reality_gem = 8

# The number seen in the unscrambled message
space_gem = 3000

# The value of third_divisible_check that you discovered in your research
time_gem = 400

# The value of you entered into power_level_generator that got you over 9000
power_gem = 9

# Enter the escape velocity value you saw once the code was fixed
soul_gem = 11187

# Go back to your code, and figure out which potential team
# is valid and has the most team members
# Once you have the largest valid team, enter the number of team members
mind_gem = 6

the_final_prize = (
    "Xli$Mrjmrm1T]$XLSR1xpix$mw$}syvw%$$$$$$$$$$$c$c$c$c$$$$$$$$$$4444$$$$$$$$$"
    "3+1,4-1+$$$$$$$$$`4$$$+$$$$$$$$$$$$$`$$2+2$$3$$$$$$$$$$$$$$$$")


# This uses your values to determine a number needed to unscramble your prize
final_value = soul_gem - (power_gem + reality_gem)
final_value += mind_gem * 5
final_value /= time_gem
final_value = space_gem % final_value
final_value = int(final_value)


descrambled_prize = [chr(ord(i)-final_value) for i in the_final_prize]

print(''.join(map(str, descrambled_prize)))