
import torch
import torch.nn as nn
from torchvision.models.video import r3d_18
from transformers import Wav2Vec2Model

class RandomFrameClassifier(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        backbone = r3d_18(weights="KINETICS400_V1")
        self.visual_backbone = nn.Sequential(
            *list(backbone.children())[:-2],
            nn.AdaptiveAvgPool3d((None, 1, 1)),
            nn.Flatten(start_dim=2)
        )
        for param in self.visual_backbone.parameters():
            param.requires_grad = False

        self.frame_projection = nn.Linear(512, 512)
        self.frame_attention = nn.MultiheadAttention(512, 8, dropout=0.1, batch_first=True)
        self.layer_norm = nn.LayerNorm(512)

        self.audio_backbone = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")
        for param in self.audio_backbone.parameters():
            param.requires_grad = False

        self.audio_projection = nn.Sequential(
            nn.Linear(768, 512),
            nn.ReLU()
        )

        self.classifier = nn.Sequential(
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    def forward(self, video_frames, audio):
        B, C, T, H, W = video_frames.shape
        video_features = self.visual_backbone(video_frames)
        video_features = video_features.permute(0, 2, 1)
        video_features = self.frame_projection(video_features)

        attn_output, _ = self.frame_attention(video_features, video_features, video_features)
        visual_features = self.layer_norm(attn_output.mean(dim=1))

        audio_features = self.audio_backbone(audio).last_hidden_state
        audio_features = audio_features.mean(dim=1)
        audio_features = self.audio_projection(audio_features)

        combined = torch.cat([visual_features, audio_features], dim=1)
        return self.classifier(combined)
