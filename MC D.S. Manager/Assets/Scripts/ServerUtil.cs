using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using HtmlAgilityPack;

public class ServerUtil{
    public static async Task<List<string>> getVersions() {
        string url = "https://minecraft.fandom.com/wiki/Bedrock_Dedicated_Server";
        List<string> versions = new List<string>();
        var web = new HtmlWeb();
        try {
            var document = await web.LoadFromWebAsync(url);
            var nodes = document.DocumentNode.SelectNodes("//*[@id='mw-content-text']/div/table[2]/tbody/tr[position()>8]/th/a");
            foreach (var node in nodes) {
                versions.Add(cutTitle(HtmlEntity.DeEntitize(node.GetAttributeValue("title", ""))));
            }
        } catch (System.Exception e) {
            Debug.Log("Connection Interrupted");
        }
        return versions;
    }


    private static string cutTitle(string title) {
        title = title.Substring(16);
        if (!(System.Char.IsNumber(title[0]))) {
            title = title.Substring(5);
        }
        return title;
    }
}
