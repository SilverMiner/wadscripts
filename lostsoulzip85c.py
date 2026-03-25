#SilverMiner Chat uses Windows XP (https://www.youtube.com/watch?v=tfZEXJj3-18) midi file playback
import base64

def encode_and_split(filename, chunk_size=195):
    with open(filename, 'rb') as f:
        data = f.read()
    
    encoded = base64.b85encode(data).decode('ascii')
    
    # Полная команда
    full_cmd = f"py -c \"import base64, zipfile, io; z=base64.b85decode('{encoded}'); zipfile.ZipFile(io.BytesIO(z)).extract('Lost Soul.mid')\""
    
    print(f"=== Файл: {filename} ===")
    print(f"Длина base85: {len(encoded)} символов")
    print(f"Длина полной команды: {len(full_cmd)} символов")
    print(f"Количество частей: {(len(full_cmd) + chunk_size - 1) // chunk_size}")
    print("\n=== ВВОДИ ПОСЛЕДОВАТЕЛЬНО ===\n")
    print("!combo win+r !send cmd\n")
    
    for i, start in enumerate(range(0, len(full_cmd), chunk_size)):
        chunk = full_cmd[start:start + chunk_size]
        print(f"!say {chunk}")
    print('!key enter')
    print('!send mplay32 /play "Lost Soul.mid"\n')

encode_and_split('Lost Soul.zip')

#the recipe is:
'''
!combo win+r !send cmd
!say py -c "import base64, zipfile, io; z=base64.b85decode('P)h>@6aWAK2mqUDN>@*mbx0`%004_J000dD002yHb95k6Z*^=gZE0lfT0u`6M-+afD5|Pd<y3DHf;X{&wT-=FKv;-FttL{qprtB@rWX$lR;ZHHkx3PC8ktBrajAMq?)?S*2T?Em75xwW
!say 1@z4~yJpDR@tV5Wg_Y3w&G)`}Z{FM4w=<J$?d<On(RG@lX_8wz?Wf%Po=&FL@3)(~FPnSr4~On{>s7Pu-rsMv_YT}@MY!JMf?Hi*UtV%ITd$t|_|p^jLF<Y8?cu@8=JNv{Omy<-8XG$K=9BA>_~*On>1)oXbmEio@a5l3`s_jb=jZNDd-w6vKk1#PsH!Nhghx~*
!say %9ED4O>u(*q?!^2tkKc-uqLh=o~CSQJeIP~45$uxPF~G`Is+3kUf8-A<6wX@tjiQn@f5#0IKZ?j4}<qe8TTui4K<01rZU1^Eql-!Lk2P3e2kfF6stf8`D6B5G1&<%Q01et7j?Zs%(Jp~ZMt6KQG<NNZT3JWCdQ9x;~s5<y9GrhbPGf!3(;f?<dwYw8V9=q#B^7%
!say Dps&0SZ3h^?I@V60vWOg+3Umiumj?@%Ngs;MST8U*<y-u&-45l9=1fD1JA?bzm&_6%SLXT%3Y3!eX(aT%MFdNPy)g)LJ0^91t9!(6o3@yIGpZ;weMz-*Ys47;whd4fBQi(6f1*Un@`>1In1bjNOBAP{GM_Ua1?EyLf~QZ>ghsoJYYgzkMA7F);FWSg+x=g@Da>p
!say V1laPRKe+&pc*)}KC_C?B-z(Do|DUL4SOA#4;SK4vaEe^gOeY&S*!J}_A9FmthQmbEvr?hZTI5)^S|h1>c&>{S!?gmTz&sWf6URZen4x1^oiE^FCagVEcj<+Sqn%6lC25tx~D8hWan7s6cyExn<FZcEGo)zr%05e9vT6~(e{OoAzumTba-(juTL8!uv|(AFUAoG
!say M)lw%7?sGEP-X)tggFfTm%b9jb+pYLrkb{jinXk0O?6%@V>!juW&H+qUX<}V@!75vwT85;onkaYMLa#zR&WfAEOEC}ui_Xv{uzw*5sb{&#4W9{x*wUZ2}|qmCavcwp2LsvwNktG;XOi}2yx;_9*DUG@)1RnQHzLi5#0scDJ_Jx!Q@ToB%2I`h!Y`>uT0)Fg1l*K
!say 6<A{nkR8aH>4D~j9LAkWn07w0I@WB*8FhT|;K4B2!Lwn$0|J?w1fc_WDvFKh3a5=|nL~3Hkg-J_HIiU)%&NwceiLRn7X{o?E@IPPMA<E1eg)$@ioA427OBnD<`uK~R$wpACOUOrZ(llf-eCIy|LC{2Qx^g6xcLYF%3ilO=&J#h1G%d22xX2>%$UU+GSh&I*QUG~
!say &1<qIOB)SmgXm#HJfu+GY>3TBw%ZHfn2Bvfb!;F%iA@vv#z^Ds&J*7PX}%X+hs#PX;Hq|B(UOw$L`z{Tvd05BJ>{+H|K9ZV?!kdM<I($l`X!^}9Iqv=?7Si}M02R$Y@QWaTak?v4ix$>i4_hMd0Y`>lz=JO!_>w2klfAkP{x%sTDCOHe?W}Zn42{I`#JqAL<S*d
!say G*398EG$HflykJ5m^vy>>hc`sl5q5XSbq~tJFmpNt`&O2W@LlkRpM?W^Bb0pkT~<6689nwzjAXC9=Gq|#w&@1StVv8+2Dp_TmJvfKk=g)6=y7~EW;lbU?|LI2TCB9U7s*jqvDL|DJP_kfn!?p7T!_fPBbcIUOwif+oGmECdP-}a^F_+Hqk95ZxP*8@+Rz{0^uvb
!say XQzJvP)h*<6aW+e000O8n`uf{Pn2~?DFpxki!uNJ4FCWD00000001BW00000002yHb95k6Z*^=gZE0jsO9ci1000010096y0000~1poj500'); zipfile.ZipFile(io.BytesIO(z)).extract('Lost Soul.mid')"
!key enter
!send mplay32 /play "Lost Soul.mid"
'''
