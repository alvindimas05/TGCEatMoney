// 1  = Hand  
// 3  = Hug  
// 4  = HighFive  
// 5  = FistBump  
// 6  = DoubleFive  
// 7  = Hug_WhiteKid  
// 8  = Hug_Lv2  
// 9  = HighFive_Lv2  
// 10 = FistBump_Lv2  
// 11 = DoubleFive_Lv2  
// 12 = Carry  
// 13 = Carry_Lv2  
// 14 = HairTousle  
// 15 = HairTousle_Lv2  
// 16 = PlayFight  
// 17 = PlayFight_Lv2  
// 18 = BearHug  
// 19 = BearHug_Lv2  
// 20 = DuetDance  
// 21 = DuetDance_Lv2  
// 22 = HandShake  
// 23 = HandShake_Lv2  
// 24 = SideHug  
// 25 = SideHug_Lv2  
// 27 = CradleCarry  
// 28 = CradleCarry_Lv2  
// 29 = DuetBow  
// 30 = DuetBow_Lv2

const emote = 13;
const baseAddr = Process.findModuleByName("Sky.exe").base;

var offset = ptr("0x1A3AB30");
var targetAddr = baseAddr.add(offset);

Interceptor.attach(targetAddr, {
    onEnter: function (args) {
        args[1] = ptr(emote.toString());
        args[2] = ptr("41249");
    }
});