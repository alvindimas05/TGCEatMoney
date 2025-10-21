// Replace with actual base address from IDA or calculate dynamically
const baseAddress = Process.findModuleByName("Sky.exe").base;
const targetAddress = baseAddress.add(ptr("0x1C82E20"));

console.log("[*] Base address:", baseAddress);
console.log("[*] Target function:", targetAddress);

Interceptor.attach(targetAddress, {
    onEnter: function(args) {
        const a1 = args[0];
        const a2 = args[1];
        const a3 = args[2];
        
        console.log("\n[+] Function called!");
        console.log("    a1 (auth context):", a1);
        console.log("    a2:", a2);
        console.log("    a3 (json output):", a3);
        
        // Read important offsets from a1
        try {
            const cryptoContextPtr = a1.add(0x96).readPointer();
            console.log("    a1+96 (crypto context):", cryptoContextPtr);
            
            const authType = a1.add(0x104).readU32();
            console.log("    a1+104 (auth type):", authType);
            
            const timestamp = a1.add(0x352).readU32();
            console.log("    a1+352 (timestamp):", timestamp);
            
            // Try to read crypto context vtable
            if (!cryptoContextPtr.isNull()) {
                const vtable = cryptoContextPtr.readPointer();
                console.log("    Crypto vtable:", vtable);
                
                const getPublicKeyFunc = vtable.add(0x328).readPointer();
                const signDataFunc = vtable.add(0x336).readPointer();
                console.log("    get_public_key (+328):", getPublicKeyFunc);
                console.log("    sign_data (+336):", signDataFunc);
            }
            
            // Dump first 1024 bytes of a1 for analysis
            console.log("\n[*] a1 memory dump:");
            console.log(hexdump(a1, { length: 1024, ansi: true }));
            
        } catch(e) {
            console.log("[-] Error reading memory:", e);
        }
    },
    
    onLeave: function(retval) {
        console.log("[+] Function returned:", retval);
    }
});

console.log("[*] Hook installed. Waiting for login...");