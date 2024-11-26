using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TelegremBot
{
    static class MessageInfo // заполнить поля RusMessage и EnMessage
    {
        private static Dictionary<TypeErrorMessage, string> RusMessage = new Dictionary<TypeErrorMessage, string>()
        {
            { TypeErrorMessage.WriteTextFound ,"Не праввильный ввод данных,попробуйте ввести данные еще раз!" },
            { TypeErrorMessage.TaskAdded,"qwe" },
            { TypeErrorMessage.TaskDeleted,"qwe" },
            { TypeErrorMessage.NeedCharSimbol,"qwe" },

        };

        private static Dictionary<TypeErrorMessage, string> EnMessage = new Dictionary<TypeErrorMessage, string>()
        {
            { TypeErrorMessage.WriteTextFound ,"Не праввильный ввод данных,попробуйте ввести данные еще раз!" },
            { TypeErrorMessage.TaskAdded,"qwe" },
            { TypeErrorMessage.TaskDeleted,"qwe" },
            { TypeErrorMessage.NeedCharSimbol,"qwe" },
        };

    }
    public enum TypeErrorMessage
    {
        WriteTextFound = 1,
        TaskAdded,
        TaskDeleted,
        NeedCharSimbol,
        
        
    }

}
