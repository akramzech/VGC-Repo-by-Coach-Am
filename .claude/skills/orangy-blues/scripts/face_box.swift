// Usage: swiftc -O face_box.swift -o /tmp/face_box && /tmp/face_box frame.png
// Prints the largest face box in pixels: x y w h (origin top-left) using Apple Vision.
import Foundation
import Vision
import AppKit
let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("ERR load"); exit(1) }
let W = Double(cg.width), H = Double(cg.height)
let req = VNDetectFaceRectanglesRequest()
try VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
guard let r = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { print("ERR noface"); exit(2) }
let b = r.boundingBox
print(String(format: "%.0f %.0f %.0f %.0f", b.minX*W, (1-b.maxY)*H, b.width*W, b.height*H))
