<?php
/**
 * Écriture d'un classeur Excel (.xlsx) sans bibliothèque externe.
 *
 * Un .xlsx est une archive zip de fichiers XML : on écrit le strict
 * nécessaire (feuilles, styles, filtres, volets figés, largeurs). Les
 * textes sont des chaînes « en ligne », jamais des formules : un nom qui
 * commence par = reste du texte, sans risque d'exécution dans Excel.
 */

declare(strict_types=1);
defined('SUBLIME') || exit;

final class SbXlsx
{
    // index des styles (cellXfs) — voir styles()
    public const S_DEFAULT = 0;
    public const S_HEADER  = 1;
    public const S_TEXT    = 2;
    public const S_DATE    = 3;
    public const S_WAIT    = 4;
    public const S_YES     = 5;
    public const S_NO      = 6;
    public const S_FAIL    = 7;
    public const S_TITLE   = 8;
    public const S_MUTED   = 9;
    public const S_BIG     = 10;
    public const S_NUM     = 11;
    public const S_LABEL   = 12;
    public const S_BOLD    = 13;

    private array $sheets = [];

    public static function available(): bool
    {
        return class_exists('ZipArchive');
    }

    /**
     * @param list<list<mixed>> $rows  cellule = valeur, ou [valeur, style]
     *        valeur : string, int|float, DateTimeInterface, ou null
     * @param array{widths?:list<float>, freeze?:bool, filter?:bool, heights?:array<int,float>} $opt
     */
    public function addSheet(string $name, array $rows, array $opt = []): void
    {
        $this->sheets[] = [$name, $rows, $opt];
    }

    /** Envoie le classeur au navigateur. */
    public function download(string $filename): never
    {
        $tmp = tempnam(sys_get_temp_dir(), 'sbx');
        $zip = new ZipArchive();
        $zip->open($tmp, ZipArchive::OVERWRITE);
        $n = count($this->sheets);

        $zip->addFromString('[Content_Types].xml',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          . '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          . '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          . '<Default Extension="xml" ContentType="application/xml"/>'
          . '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          . '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
          . implode('', array_map(fn ($i) => '<Override PartName="/xl/worksheets/sheet' . $i . '.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>', range(1, $n)))
          . '</Types>');

        $zip->addFromString('_rels/.rels',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          . '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
          . '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
          . '</Relationships>');

        $sheetsXml = $rels = '';
        foreach ($this->sheets as $i => [$name]) {
            $k = $i + 1;
            $sheetsXml .= '<sheet name="' . $this->esc(sb_cut($name, 31)) . '" sheetId="' . $k . '" r:id="rId' . $k . '"/>';
            $rels .= '<Relationship Id="rId' . $k . '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet' . $k . '.xml"/>';
        }
        $rels .= '<Relationship Id="rId' . ($n + 1) . '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>';

        $zip->addFromString('xl/workbook.xml',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          . '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          . '<bookViews><workbookView activeTab="0"/></bookViews><sheets>' . $sheetsXml . '</sheets></workbook>');
        $zip->addFromString('xl/_rels/workbook.xml.rels',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          . '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' . $rels . '</Relationships>');
        $zip->addFromString('xl/styles.xml', $this->styles());

        foreach ($this->sheets as $i => [$name, $rows, $opt]) {
            $zip->addFromString('xl/worksheets/sheet' . ($i + 1) . '.xml', $this->sheet($rows, $opt, $i === 0));
        }
        $zip->close();

        header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        header('Content-Disposition: attachment; filename="' . $filename . '"');
        header('Content-Length: ' . filesize($tmp));
        readfile($tmp);
        @unlink($tmp);
        exit;
    }

    // ------------------------------------------------------------ feuille

    private function sheet(array $rows, array $opt, bool $selected): string
    {
        $cols = 0;
        foreach ($rows as $r) {
            $cols = max($cols, count($r));
        }
        $x = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           . '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">';
        $x .= '<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>';   // impression : une page de large
        $x .= '<sheetViews><sheetView workbookViewId="0" showGridLines="0"' . ($selected ? ' tabSelected="1"' : '') . '>';
        if (!empty($opt['freeze'])) {
            $x .= '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>';
        }
        $x .= '</sheetView></sheetViews><sheetFormatPr defaultRowHeight="18"/>';

        if (!empty($opt['widths'])) {
            $x .= '<cols>';
            foreach ($opt['widths'] as $i => $w) {
                $x .= '<col min="' . ($i + 1) . '" max="' . ($i + 1) . '" width="' . $w . '" customWidth="1"/>';
            }
            $x .= '</cols>';
        }

        $x .= '<sheetData>';
        foreach (array_values($rows) as $ri => $row) {
            $r = $ri + 1;
            $ht = $opt['heights'][$ri] ?? null;
            $x .= '<row r="' . $r . '"' . ($ht ? ' ht="' . $ht . '" customHeight="1"' : '') . '>';
            foreach (array_values($row) as $ci => $cell) {
                [$v, $s] = is_array($cell) ? [$cell[0], $cell[1] ?? 0] : [$cell, 0];
                $ref = $this->col($ci) . $r;
                if ($v === null || $v === '') {
                    $x .= $s ? '<c r="' . $ref . '" s="' . $s . '"/>' : '';
                } elseif ($v instanceof DateTimeInterface) {
                    $x .= '<c r="' . $ref . '" s="' . ($s ?: self::S_DATE) . '"><v>' . $this->serial($v) . '</v></c>';
                } elseif (is_int($v) || is_float($v)) {
                    $x .= '<c r="' . $ref . '" s="' . $s . '"><v>' . $v . '</v></c>';
                } else {
                    $x .= '<c r="' . $ref . '" s="' . $s . '" t="inlineStr"><is><t xml:space="preserve">'
                        . $this->esc((string) $v) . '</t></is></c>';
                }
            }
            $x .= '</row>';
        }
        $x .= '</sheetData>';

        if (!empty($opt['filter']) && count($rows) > 1 && $cols) {
            $x .= '<autoFilter ref="A1:' . $this->col($cols - 1) . count($rows) . '"/>';
        }
        $x .= '<pageMargins left="0.5" right="0.5" top="0.6" bottom="0.6" header="0.3" footer="0.3"/>'
            . '<pageSetup paperSize="1" orientation="landscape" fitToWidth="1" fitToHeight="0"/>';
        return $x . '</worksheet>';
    }

    // ------------------------------------------------------------ styles

    private function styles(): string
    {
        $fonts = [
            '<font><sz val="11"/><name val="Calibri"/></font>',                                       // 0
            '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>',            // 1 en-tête
            '<font><b/><sz val="11"/><color rgb="FF9A5300"/><name val="Calibri"/></font>',            // 2 attente
            '<font><b/><sz val="11"/><color rgb="FF0B6B43"/><name val="Calibri"/></font>',            // 3 oui
            '<font><b/><sz val="11"/><color rgb="FF6B778D"/><name val="Calibri"/></font>',            // 4 non
            '<font><b/><sz val="11"/><color rgb="FFB31942"/><name val="Calibri"/></font>',            // 5 échec
            '<font><b/><sz val="18"/><color rgb="FF0A3161"/><name val="Calibri"/></font>',            // 6 titre
            '<font><i/><sz val="10"/><color rgb="FF6B778D"/><name val="Calibri"/></font>',            // 7 discret
            '<font><b/><sz val="14"/><color rgb="FF0A3161"/><name val="Calibri"/></font>',            // 8 chiffre
            '<font><sz val="11"/><color rgb="FF16223A"/><name val="Calibri"/></font>',                // 9 libellé
            '<font><b/><sz val="11"/><name val="Calibri"/></font>',                                   // 10 gras
        ];
        $fill = fn (string $rgb) => '<fill><patternFill patternType="solid"><fgColor rgb="FF' . $rgb . '"/><bgColor indexed="64"/></patternFill></fill>';
        $fills = [
            '<fill><patternFill patternType="none"/></fill>',     // 0 (réservé)
            '<fill><patternFill patternType="gray125"/></fill>',  // 1 (réservé)
            $fill('0A3161'),  // 2 marine
            $fill('FFF1DF'),  // 3 attente
            $fill('E8F6EF'),  // 4 oui
            $fill('F1F2F5'),  // 5 non
            $fill('FBEAEF'),  // 6 échec
        ];
        $borders = [
            '<border><left/><right/><top/><bottom/><diagonal/></border>',
            '<border><left/><right/><top/><bottom style="thin"><color rgb="FFE2E7EF"/></bottom><diagonal/></border>',
        ];
        $al = fn (string $h = 'left', bool $wrap = false) => '<alignment horizontal="' . $h . '" vertical="center"' . ($wrap ? ' wrapText="1"' : '') . '/>';
        $xf = fn (int $font, int $fill, int $border, int $num, string $align) =>
            '<xf numFmtId="' . $num . '" fontId="' . $font . '" fillId="' . $fill . '" borderId="' . $border . '" xfId="0"'
            . ($num ? ' applyNumberFormat="1"' : '') . ' applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">' . $align . '</xf>';
        $xfs = [
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>',   // 0
            $xf(1, 2, 0, 0, $al('left', true)),                                // 1 en-tête
            $xf(0, 0, 1, 0, $al('left', true)),                                // 2 texte
            $xf(0, 0, 1, 164, $al('left')),                                    // 3 date
            $xf(2, 3, 1, 0, $al('center')),                                    // 4 attente
            $xf(3, 4, 1, 0, $al('center')),                                    // 5 oui
            $xf(4, 5, 1, 0, $al('center')),                                    // 6 non
            $xf(5, 6, 1, 0, $al('center')),                                    // 7 échec
            $xf(6, 0, 0, 0, $al('left')),                                      // 8 titre
            $xf(7, 0, 0, 0, $al('left')),                                      // 9 discret
            $xf(8, 0, 1, 0, $al('center')),                                    // 10 chiffre
            $xf(0, 0, 1, 1, $al('center')),                                    // 11 nombre
            $xf(9, 0, 1, 0, $al('left')),                                      // 12 libellé
            $xf(10, 0, 1, 0, $al('left', true)),                               // 13 gras
        ];
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             . '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             . '<numFmts count="1"><numFmt numFmtId="164" formatCode="dd/mm/yyyy hh:mm"/></numFmts>'
             . '<fonts count="' . count($fonts) . '">' . implode('', $fonts) . '</fonts>'
             . '<fills count="' . count($fills) . '">' . implode('', $fills) . '</fills>'
             . '<borders count="' . count($borders) . '">' . implode('', $borders) . '</borders>'
             . '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
             . '<cellXfs count="' . count($xfs) . '">' . implode('', $xfs) . '</cellXfs>'
             . '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
             . '</styleSheet>';
    }

    // ------------------------------------------------------------ outils

    private function col(int $i): string
    {
        $s = '';
        for ($i++; $i > 0; $i = intdiv($i - 1, 26)) {
            $s = chr(65 + ($i - 1) % 26) . $s;
        }
        return $s;
    }

    /** Date Excel : jours depuis le 30/12/1899, à l'heure locale affichée. */
    private function serial(DateTimeInterface $d): string
    {
        $local = (int) $d->format('U') + (int) $d->format('Z');
        return rtrim(rtrim(sprintf('%.10F', round($local) / 86400 + 25569), '0'), '.');
    }

    private function esc(string $v): string
    {
        $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F]/u', '', $v) ?? '';
        return htmlspecialchars($v, ENT_QUOTES | ENT_XML1, 'UTF-8');
    }
}
