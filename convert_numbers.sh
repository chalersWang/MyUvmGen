#!/bin/bash
# ============================================================
# MyUvmGen_v2.0_macos — Numbers → Excel 转换工具
#
# 用法:
#   chmod +x convert_numbers.sh
#   ./convert_numbers.sh VerifyEnvironmentGenCfg_canfd.numbers
#
# 输出: 同目录下的 VerifyEnvironmentGenCfg_canfd.xlsx
# ============================================================
set -e

INPUT="$1"
if [ -z "$INPUT" ]; then
    echo "用法: $0 <file.numbers>"
    echo "示例: $0 VerifyEnvironmentGenCfg_canfd.numbers"
    exit 1
fi

ABS_INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
OUTPUT="${ABS_INPUT%.numbers}.xlsx"

echo "输入: $ABS_INPUT"
echo "输出: $OUTPUT"

# 方式1: 尝试 python numbers-parser
echo "尝试 numbers-parser..."
python3 -c "
import sys
try:
    from numbers_parser import Document
    doc = Document('$ABS_INPUT')
    
    # 导出所有 sheet
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # 删除默认 sheet
    
    for s in doc.sheets:
        ws = wb.create_sheet(title=s.name)
        for table in s.tables:
            for ri, row in enumerate(table.rows(), 1):
                for ci, cell in enumerate(row, 1):
                    ws.cell(row=ri, column=ci, value=cell.value)
    
    wb.save('$OUTPUT')
    print('✅ 转换完成: $OUTPUT')
except ImportError as e:
    print(f'numbers-parser 不可用: {e}')
    sys.exit(1)
" 2>/dev/null && exit 0

# 方式2: AppleScript + Numbers.app
echo "使用 Numbers.app 转换..."
osascript << APPLESCRIPT
on run
    set inputPath to POSIX file "$ABS_INPUT"
    set outputPath to POSIX file "$OUTPUT"
    
    tell application "Numbers"
        activate
        set theDoc to open inputPath
        delay 2
        export theDoc to outputPath as Microsoft Excel
        close theDoc without saving
    end tell
    
    return "✅ 转换完成: $OUTPUT"
end run
APPLESCRIPT

echo ""
echo "============================================"
echo "转换完成: $OUTPUT"
echo "现在可以运行主脚本:"
echo "  cd $(dirname "$0")"
echo "  python3 UvmEnvironmentGen.py $OUTPUT"
