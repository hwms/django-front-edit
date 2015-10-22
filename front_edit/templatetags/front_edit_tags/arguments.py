from __future__ import unicode_literals

from classytags.arguments import MultiValueArgument

from front_edit.compat import unpack


class NonGreedyMultiValueArgument(MultiValueArgument):
    def parse(self, parser, token, tagname, kwargs):
        """
        Parse a token.
        """
        value = self.value_class(self.parse_token(parser, token))
        literal, options = unpack(value.literal.split(':', 1))
        if literal.find('.') == -1:
            return False
        if self.name in kwargs:
            if self.max_values and len(kwargs[self.name]) == self.max_values:
                return False
            kwargs[self.name].append(value)
        else:
            kwargs[self.name] = self.sequence_class(value)
        return True
