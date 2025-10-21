const baseAddr = Process.findModuleByName("Sky.exe").base;

console.log("Base address of Sky.exe:", baseAddr);

var funcAddr = baseAddr.add(ptr("0x17BB9E0"));
Interceptor.attach(funcAddr, {
    onEnter: function(args) {
        var rdi = args[0];  // This IS _RDI (a1)
        console.log("_RDI (a1):", rdi);
        
        // Read the level name from it
        var stringAddr = rdi.add(80);
        var capacity = rdi.add(104).readU64();
        
        var stringValue;
        if (capacity < 16) {
            stringValue = stringAddr.readUtf8String();
        } else {
            stringValue = stringAddr.readPointer().readUtf8String();
        }
        
        console.log("Level name:", stringValue);
    }
});