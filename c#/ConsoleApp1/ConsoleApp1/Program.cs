using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.ComTypes;
using System.Text;
using System.Threading.Tasks;

namespace laith
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string strVar = "assem pro gaming pro code mohamed assem dkhissi lol man laith ";
            string[] strVarArray = strVar.Split(' ');

            for (int i = 0; i < strVarArray.Length; i++)
            {
                Console.WriteLine(strVarArray[i]);
                char[] charVarArray = strVarArray[i].ToCharArray();

                for (int j = 0; j < charVarArray.Length; j++)
                {
                    Console.Write("   {0}", charVarArray[j]);
                }

                Console.Write("\n");
            }
        }
    }
}