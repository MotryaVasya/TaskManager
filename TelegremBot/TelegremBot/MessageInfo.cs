using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TelegremBot
{
    static class MessageInfo // заполнить поля RusMessage и EnMessage
    {
        private static Dictionary<string, string> RusMessage = new Dictionary<string, string>()
        {
            { "we","qwe" },
            { "we","qwe" },
            { "we","qwe" },
            { "we","qwe" },

        };

        private static Dictionary<string, string> EnMessage = new Dictionary<string, string>()
        {
            { "we","qwe" },
            { "we","qwe" },
            { "we","qwe" },
            { "we","qwe" },
        };

    }
    public enum Type
    {
        None,
        empty
    }

}
